document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("upload-form");
  const resultsDiv = document.getElementById("results");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const input = document.getElementById("files");
    const formData = new FormData();

    for (const file of input.files) {
      formData.append("files", file);
    }

    const res = await fetch("/upload/", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    resultsDiv.innerHTML = "";

    data.results.forEach(result => {
      const container = document.createElement("div");
      container.className = "bg-gray-100 p-4 rounded-md shadow";

      const img = document.createElement("img");
      img.src = result.image_url;
      img.alt = "Uploaded gesture";
      img.className = "w-full h-64 object-contain rounded";

      const labelBox = document.createElement("div");
      labelBox.className = "mt-4 space-y-1";

      result.predictions.forEach(pred => {
        const p = document.createElement("p");
        p.innerText = `Prediction: ${pred.label} (${pred.confidence})`;
        p.className = "text-gray-700 text-sm";
        labelBox.appendChild(p);
      });

      container.appendChild(img);
      container.appendChild(labelBox);
      resultsDiv.appendChild(container);
    });
  });
});