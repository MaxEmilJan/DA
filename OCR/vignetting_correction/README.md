These two files are used to correct the vignetting effect.

create_correction_mask.py

Therefore a reference image must be taken. A white background would be best, since the vignetting effect at the outside of the picture will be visible best for brighter images.
This image can be loaded and processed with this file, to create an array which contains values to counter the vignetting effect.


vignetting_correction.py

The reciprocal of the created mask must be multiplied pixelwise to the image you want to remove the vignetting from. This is done here. The corrected image is saved in an array, which can be used for further processing (e.g. OCR)
