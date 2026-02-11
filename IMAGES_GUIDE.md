# Hero Background Images Guide

## Image Requirements

To add background images to your hero sections, place the following images in the `images/` folder:

### Required Images:

1. **hero_tech_background.jpg** (1920x600px)
   - For homepage hero section
   - Suggested: Modern tech background with circuit patterns, blue/purple neon lights
   - Dark theme to match the design

2. **page_header_background.jpg** (1920x600px)
   - For all page headers (Products, Warranty, Contact)
   - Suggested: Abstract technology patterns, laptop/computer imagery
   - Dark theme with subtle tech elements

### Image Specifications:

- **Format**: JPG or PNG
- **Dimensions**: 1920x600 pixels (wide banner format)
- **File Size**: Keep under 500KB for fast loading
- **Color Scheme**: Dark backgrounds with blue/purple accents
- **Opacity**: Images will be displayed at 12-15% opacity over dark gradients

### Where to Find Images:

You can use free stock photo sites like:
- Unsplash.com (search: "technology background", "circuit board", "tech workspace")
- Pexels.com (search: "dark tech", "neon technology", "computer background")
- Pixabay.com (search: "technology pattern", "digital background")

### Current Setup:

The CSS is already configured to use these images. Once you add the image files to the `images/` folder, they will automatically appear as backgrounds with the proper styling applied.

If images are not present, the site will still look great with the gradient and pattern backgrounds that are currently active.

### CSS Classes Using Background Images:

- `.hero::before` - Homepage hero section background
- `.page-header::before` - All page headers background

You can also customize individual page headers by adding specific classes if needed.
