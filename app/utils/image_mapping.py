"""
Image mapping utility for user profiles.
Using placeholder images from UI Faces API for demonstration.
In production, you should use your own image hosting service.
"""

MALE_PROFILE_IMAGES = [
    "https://randomuser.me/api/portraits/men/1.jpg",
    "https://randomuser.me/api/portraits/men/2.jpg",
    "https://randomuser.me/api/portraits/men/3.jpg",
    "https://randomuser.me/api/portraits/men/4.jpg",
    "https://randomuser.me/api/portraits/men/5.jpg",
    "https://randomuser.me/api/portraits/men/6.jpg",
    "https://randomuser.me/api/portraits/men/7.jpg",
    "https://randomuser.me/api/portraits/men/8.jpg",
    "https://randomuser.me/api/portraits/men/9.jpg",
    "https://randomuser.me/api/portraits/men/10.jpg",
]

FEMALE_PROFILE_IMAGES = [
    "https://randomuser.me/api/portraits/women/1.jpg",
    "https://randomuser.me/api/portraits/women/2.jpg",
    "https://randomuser.me/api/portraits/women/3.jpg",
    "https://randomuser.me/api/portraits/women/4.jpg",
    "https://randomuser.me/api/portraits/women/5.jpg",
    "https://randomuser.me/api/portraits/women/6.jpg",
    "https://randomuser.me/api/portraits/women/7.jpg",
    "https://randomuser.me/api/portraits/women/8.jpg",
    "https://randomuser.me/api/portraits/women/9.jpg",
    "https://randomuser.me/api/portraits/women/10.jpg",
]

OTHER_PROFILE_IMAGES = [
    "https://randomuser.me/api/portraits/lego/1.jpg",
    "https://randomuser.me/api/portraits/lego/2.jpg",
    "https://randomuser.me/api/portraits/lego/3.jpg",
    "https://randomuser.me/api/portraits/lego/4.jpg",
    "https://randomuser.me/api/portraits/lego/5.jpg",
]

def get_random_image_for_gender(gender: str, used_images: set) -> str:
    """
    Get a random image URL for the specified gender that hasn't been used yet.
    
    Args:
        gender: The gender of the user ('Male', 'Female', or 'Other')
        used_images: Set of already used image URLs
    
    Returns:
        str: URL of the selected image
    """
    if gender.lower() == 'male':
        available_images = [img for img in MALE_PROFILE_IMAGES if img not in used_images]
    elif gender.lower() == 'female':
        available_images = [img for img in FEMALE_PROFILE_IMAGES if img not in used_images]
    else:
        available_images = [img for img in OTHER_PROFILE_IMAGES if img not in used_images]
    
    if not available_images:
        # If all images are used, start over with the full set
        if gender.lower() == 'male':
            return MALE_PROFILE_IMAGES[0]
        elif gender.lower() == 'female':
            return FEMALE_PROFILE_IMAGES[0]
        else:
            return OTHER_PROFILE_IMAGES[0]
    
    import random
    return random.choice(available_images) 