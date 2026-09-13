"""YOLO-based wildlife detection from camera trap images."""
import cv2
import numpy as np
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class WildlifeDetector:
    """Detect and count wildlife in images using YOLO."""

    WILDLIFE_CLASSES = {
        'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant',
        'bear', 'zebra', 'giraffe', 'deer', 'monkey', 'leopard',
        'tiger', 'rhinoceros', 'hippopotamus', 'crocodile', 'snake',
        'turtle', 'lizard', 'frog', 'toad'
    }

    def __init__(self, model_path: str = "yolov8m.pt", confidence: float = 0.5):
        self.confidence = confidence
        self._model = None
        self._model_path = model_path

    @property
    def model(self):
        if self._model is None:
            try:
                from ultralytics import YOLO
                self._model = YOLO(self._model_path)
                logger.info(f"Loaded YOLO model: {self._model_path}")
            except ImportError:
                logger.error("ultralytics not installed. Run: pip install ultralytics")
                raise
        return self._model

    def detect(self, image_path: str | Path) -> list[dict]:
        """Detect wildlife in a single image."""
        try:
            results = self.model(str(image_path), conf=self.confidence)
            detections = []

            for result in results:
                for box in result.boxes:
                    cls_id = int(box.cls[0])
                    cls_name = result.names[cls_id]
                    conf = float(box.conf[0])

                    if cls_name.lower() in self.WILDLIFE_CLASSES:
                        detections.append({
                            "species": cls_name,
                            "confidence": round(conf, 4),
                            "bbox": {
                                "x1": round(float(box.xyxy[0][0]), 2),
                                "y1": round(float(box.xyxy[0][1]), 2),
                                "x2": round(float(box.xyxy[0][2]), 2),
                                "y2": round(float(box.xyxy[0][3]), 2),
                            },
                            "area": round(float(box.xyxy[0][2] - box.xyxy[0][0]) *
                                        float(box.xyxy[0][3] - box.xyxy[0][1]), 2),
                        })

            return detections

        except Exception as e:
            logger.error(f"Detection failed for {image_path}: {e}")
            return []

    def detect_and_count(self, image_path: str | Path) -> dict:
        """Detect wildlife and count species."""
        detections = self.detect(image_path)
        species_counts = {}

        for det in detections:
            species = det["species"]
            if species not in species_counts:
                species_counts[species] = {
                    "count": 0,
                    "avg_confidence": 0,
                    "confidences": []
                }
            species_counts[species]["count"] += 1
            species_counts[species]["confidences"].append(det["confidence"])

        for species in species_counts:
            confs = species_counts[species]["confidences"]
            species_counts[species]["avg_confidence"] = round(sum(confs) / len(confs), 4)
            del species_counts[species]["confidences"]

        return {
            "total_detections": len(detections),
            "species_counts": species_counts,
            "detections": detections,
        }

    def detect_batch(self, image_paths: list[str | Path]) -> list[dict]:
        """Detect wildlife in multiple images."""
        return [self.detect_and_count(path) for path in image_paths]

    def annotate_image(self, image_path: str | Path, output_path: Optional[Path] = None) -> Path:
        """Draw detection boxes on image and save."""
        img = cv2.imread(str(image_path))
        detections = self.detect(image_path)

        colors = {
            "bird": (0, 255, 0),
            "deer": (255, 0, 0),
            "monkey": (0, 0, 255),
            "elephant": (255, 255, 0),
            "leopard": (128, 0, 128),
            "cow": (0, 128, 255),
        }

        for det in detections:
            bbox = det["bbox"]
            color = colors.get(det["species"], (255, 255, 255))
            cv2.rectangle(img,
                         (int(bbox["x1"]), int(bbox["y1"])),
                         (int(bbox["x2"]), int(bbox["y2"])),
                         color, 2)
            label = f"{det['species']} {det['confidence']:.2f}"
            cv2.putText(img, label,
                       (int(bbox["x1"]), int(bbox["y1"]) - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        if output_path is None:
            output_path = Path(str(image_path)).parent / f"annotated_{Path(image_path).name}"

        cv2.imwrite(str(output_path), img)
        return output_path
