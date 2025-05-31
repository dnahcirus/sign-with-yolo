import React, { useState } from 'react';
import { X } from 'lucide-react';

// Importing all images
import img1 from '../img/a.jpg';
import img2 from '../img/b.jpg';
import img3 from '../img/c.jpg';
import img4 from '../img/d.jpg';
import img5 from '../img/e.jpg';
import img6 from '../img/f.jpg';
import img7 from '../img/g.jpg';
import img8 from '../img/h.jpg';
import img9 from '../img/i.jpg';
import img10 from '../img/j.jpg';

export default function Home() {
  const images = [
    { src: img1, name: 'A', description: 'Sign for A: Closed fist with thumb along the side.' },
    { src: img2, name: 'B', description: 'Sign for B: Palm open with fingers together, thumb across palm.' },
    { src: img3, name: 'C', description: 'Sign for C: Hand forms the shape of the letter C.' },
    { src: img4, name: 'D', description: 'Sign for D: Index finger up, other fingers touch thumb.' },
    { src: img5, name: 'E', description: 'Sign for E: Fingers curled with thumb underneath.' },
    { src: img6, name: 'F', description: 'Sign for F: Thumb and index finger form a circle, others up.' },
    { src: img7, name: 'G', description: 'Sign for G: Index finger and thumb pointing sideways.' },
    { src: img8, name: 'H', description: 'Sign for H: Index and middle fingers together pointing sideways.' },
    { src: img9, name: 'I', description: 'Sign for I: Pinky finger up.' },
    { src: img10, name: 'J', description: 'Sign for J: Pinky traces the shape of a J in the air.' },
  ];

  const [selectedImage, setSelectedImage] = useState(null);

  return (
    <div className="min-h-screen bg-white px-6 py-10 md:px-20 lg:px-32">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-10 items-center">
        {/* Text Section */}
        <div className="space-y-6">
          <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight">
            ASL: American Sign Language
          </h1>
          <p className="text-lg text-gray-700 leading-relaxed">
            American Sign Language (ASL) is a rich, visual language used by the Deaf community. It
            has its own grammar, syntax, and culture — offering a unique way to connect through hand
            gestures, expressions, and movement.
          </p>
        </div>

        {/* Image Grid */}
        <div className="grid grid-cols-3 gap-4">
          {images.map((img, index) => (
            <div
              key={index}
              onClick={() => setSelectedImage(img)}
              className={`
                relative overflow-hidden rounded-xl shadow hover:shadow-md transition-shadow duration-300 cursor-pointer
                ${index === 9 ? 'col-span-3 flex justify-center' : ''}
              `}
            >
              <img
                src={img.src}
                alt={`Sign language gesture ${img.name}`}
                className="object-cover w-full max-w-xs h-28 md:h-32 lg:h-36"
              />
              <div className="absolute bottom-0 left-0 right-0 bg-black/60 text-white text-sm text-center py-1">
                Gesture {img.name}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* CTA Button */}
      <div className="flex justify-center mt-16">
        <a
          href="http://localhost:8000"
          target="_blank"
          rel="noopener noreferrer"
          className="bg-blue-600 text-white px-8 py-3 rounded-full text-lg font-medium shadow-lg hover:bg-blue-700 transition"
        >
          Take the Test
        </a>
      </div>

      {/* Modal Popup */}
      {selectedImage && (
        <div className="fixed inset-0 z-50 bg-black/60 flex items-center justify-center">
          <div className="bg-white rounded-2xl shadow-xl max-w-4xl w-full p-6 relative flex flex-col md:flex-row gap-6">
            <button
              className="absolute top-4 right-4 text-gray-500 hover:text-red-500"
              onClick={() => setSelectedImage(null)}
            >
              <X size={24} />
            </button>

            {/* Left Side - Image */}
            <div className="flex-shrink-0 flex justify-center items-center w-full md:w-1/2">
              <img
                src={selectedImage.src}
                alt={selectedImage.name}
                className="rounded-xl max-h-96 object-contain"
              />
            </div>

            {/* Right Side - Details */}
            <div className="w-full md:w-1/2 flex flex-col justify-center space-y-4">
              <h2 className="text-3xl font-bold text-gray-900">Sign: {selectedImage.name}</h2>
              <p className="text-gray-700 text-base">{selectedImage.description}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}