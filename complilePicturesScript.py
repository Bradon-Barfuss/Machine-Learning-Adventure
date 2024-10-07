import os
from PIL import Image

# Directory where the images are saved
save_dir = "feature_distributions_2"



# List of features (columns) you want to stitch together
features = ['Age', 'Pclass', 'SibSp', 'Q', 'Age_Sex', 'Age_Q', 'Age_Pclass',
       'Sex_Pclass', 'Sex_SibSp', 'Sex_Parch', 'Sex_Q', 'Pclass_SibSp',
       'Pclass_Parch', 'Pclass_Q', 'SibSp_Q', 'SibSp_S', 'Parch_Q', 'Parch_S']  # Add all feature names here

# Number of folds
num_folds = 4

# Function to load images and stitch them
def stitch_images(save_dir, features, num_folds):
    # Initialize list to hold rows of images (each row corresponds to a fold)
    image_rows = []
    
    for fold_num in range(0, num_folds + 1):
        # List to hold images for this row (i.e., all features for this fold)
        row_images = []
        
        for feature in features:
            # Construct the filename for the image
            image_filename = f'FoldNumber{fold_num}__{feature}_distribution_v2.png'
            image_path = os.path.join(save_dir, image_filename)
            
            # Open the image
            img = Image.open(image_path)
            
            # Append to the row images list
            row_images.append(img)
        
        # Stitch all images in the row (horizontally)
        row_widths, row_heights = zip(*(img.size for img in row_images))
        total_row_width = sum(row_widths)
        max_row_height = max(row_heights)
        
        # Create a blank image for the stitched row
        stitched_row = Image.new('RGB', (total_row_width, max_row_height))
        
        # Paste the images next to each other
        x_offset = 0
        for img in row_images:
            stitched_row.paste(img, (x_offset, 0))
            x_offset += img.width
        
        # Append the stitched row to the image rows
        image_rows.append(stitched_row)
    
    # Stitch all rows together (vertically)
    row_widths, row_heights = zip(*(img.size for img in image_rows))
    max_row_width = max(row_widths)
    total_height = sum(row_heights)
    
    # Create a blank image for the final stitched image
    final_image = Image.new('RGB', (max_row_width, total_height))
    
    # Paste all the rows on top of each other
    y_offset = 0
    for row_img in image_rows:
        final_image.paste(row_img, (0, y_offset))
        y_offset += row_img.height
    
    # Save the final stitched image
    final_image.save(os.path.join(save_dir, 'stitched_image_grid_v2.png'))
    print(f'Successfully stitched image saved as stitched_image_grid_v2.png')

# Call the function to stitch images
stitch_images(save_dir, features, num_folds)
