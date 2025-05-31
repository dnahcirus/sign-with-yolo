import os
import csv
import torch
from ultralytics import YOLO
from tkinter import Tk, Text, Scrollbar, END, BOTH, RIGHT, Y
from threading import Thread


# === Setup GUI window for output ===
class OutputWindow:
    def __init__(self):
        self.root = Tk()
        self.root.title("YOLOv8 Training Progress")

        self.text = Text(self.root, wrap='word', font=('Consolas', 12))
        self.text.pack(expand=True, fill=BOTH)

        scrollbar = Scrollbar(self.root, command=self.text.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.text.config(yscrollcommand=scrollbar.set)

    def log(self, message: str):
        self.text.insert(END, message + '\n')
        self.text.see(END)
        self.root.update()

    def start(self, target_fn):
        Thread(target=target_fn, daemon=True).start()
        self.root.mainloop()


# === Training logic ===
class YOLOTrainer:
    def __init__(self, gui: OutputWindow):
        self.gui = gui
        self.device = (
            'cuda' if torch.cuda.is_available()
            else 'mps' if torch.backends.mps.is_available()
            else 'cpu'
        )
        self.gui.log(f"✅ Using device: {self.device.upper()}")
        if self.device == 'cuda':
            torch.cuda.empty_cache()

        self.model_name = 'yolov8_sign_detection'
        self.project_path = 'sign_detection_project2'
        self.data_path = '/Users/dnahcirus/Desktop/project/sign with yolo/dataset.yaml'
        self.checkpoint_dir = '/Users/dnahcirus/Desktop/sign with yolo/checkpoints1'
        self.log_file = os.path.join(self.checkpoint_dir, f"{self.model_name}_training_logs.csv")

        self.epochs = 5
        self.checkpoint_interval = 5
        self.imgsz = 400
        self.batch = 16

        # Check YAML file existence early
        if not os.path.exists(self.data_path):
            self.gui.log(f"❌ dataset.yaml not found at: {self.data_path}")
            raise FileNotFoundError(f"dataset.yaml missing: {self.data_path}")

        os.makedirs(self.checkpoint_dir, exist_ok=True)
        self._init_log()

        self.latest_checkpoint = self._get_latest_checkpoint()
        self.model = YOLO(self.latest_checkpoint if self.latest_checkpoint else 'yolov8n.pt')
        self.start_epoch = self._get_start_epoch()

    def _init_log(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, mode='w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Epoch', 'Box Loss', 'Class Loss', 'Object Loss',
                                 'mAP@0.5', 'mAP@0.5:0.95', 'Inference Speed', 'Postprocess Speed'])

    def _get_latest_checkpoint(self):
        for epoch in range(self.epochs, 0, -self.checkpoint_interval):
            path = os.path.join(self.checkpoint_dir, f'{self.model_name}_epoch_{epoch}.pt')
            if os.path.isfile(path):
                self.gui.log(f"🔁 Found checkpoint: {path}")
                return path
        self.gui.log("🆕 No checkpoint found. Starting from scratch.")
        return None

    def _get_start_epoch(self):
        if self.latest_checkpoint:
            try:
                return int(os.path.basename(self.latest_checkpoint).split('_')[-1].replace('.pt', ''))
            except ValueError:
                self.gui.log("⚠️ Failed to parse checkpoint epoch. Defaulting to 0.")
        return 0

    def train(self):
        while self.start_epoch < self.epochs:
            end_epoch = min(self.start_epoch + self.checkpoint_interval, self.epochs)
            self.gui.log(f"🚀 Training from epoch {self.start_epoch + 1} to {end_epoch}")

            try:
                results = self.model.train(
                    data=self.data_path,
                    epochs=end_epoch - self.start_epoch,
                    imgsz=self.imgsz,
                    batch=self.batch,
                    device=self.device,
                    project=self.project_path,
                    name=self.model_name,
                    resume=False
                )
            except Exception as e:
                self.gui.log(f"[ERROR] Training failed: {e}")
                return

            try:
                metrics = results.metrics if hasattr(results, "metrics") else {}
                box_loss = metrics.get("box", "N/A")
                cls_loss = metrics.get("cls", "N/A")
                obj_loss = metrics.get("obj", "N/A")
                map50 = metrics.get("metrics/mAP_0.5", "N/A")
                map50_95 = metrics.get("metrics/mAP_0.5:0.95", "N/A")
                speed = results.speed if hasattr(results, "speed") else {}

                with open(self.log_file, mode='a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        end_epoch, box_loss, cls_loss, obj_loss,
                        map50, map50_95,
                        speed.get('inference', 'NA'),
                        speed.get('postprocess', 'NA')
                    ])

                self.gui.log(f"✅ Metrics for epoch {end_epoch}")
                self.gui.log(f"📉 Box: {box_loss}, Class: {cls_loss}, Obj: {obj_loss}")
                self.gui.log(f"📈 mAP@0.5: {map50}, mAP@0.5:0.95: {map50_95}")
                self.gui.log(f"⚡ Inference: {speed.get('inference', 'N/A')}, Postprocess: {speed.get('postprocess', 'N/A')}")

            except Exception as e:
                self.gui.log(f"[ERROR] Failed to log metrics: {e}")

            # Save checkpoint
            ckpt_path = os.path.join(self.checkpoint_dir, f'{self.model_name}_epoch_{end_epoch}.pt')
            try:
                self.model.save(ckpt_path)
                self.gui.log(f"💾 Checkpoint saved at: {ckpt_path}")
            except Exception as e:
                self.gui.log(f"[ERROR] Failed to save checkpoint: {e}")

            # Attempt plotting
            try:
                results.plot()
            except Exception as e:
                self.gui.log(f"[WARN] Could not plot results: {e}")

            self.start_epoch = end_epoch
            if self.device == 'cuda':
                torch.cuda.empty_cache()
            self.model = YOLO(ckpt_path)


# === Main entry point ===
if __name__ == "__main__":
    gui = OutputWindow()
    trainer = YOLOTrainer(gui)
    gui.start(trainer.train)
