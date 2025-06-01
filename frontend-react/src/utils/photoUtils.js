// Unsplash API configuration
const UNSPLASH_ACCESS_KEY = 'YOUR_UNSPLASH_ACCESS_KEY';

// Cache photos in localStorage to maintain consistency during the session
const PHOTO_CACHE_KEY = 'profile_photos_cache';
const CACHE_EXPIRY = 24 * 60 * 60 * 1000; // 24 hours

// Initialize or get existing cache
const getPhotoCache = () => {
  const cached = localStorage.getItem(PHOTO_CACHE_KEY);
  if (cached) {
    const { timestamp, photos } = JSON.parse(cached);
    if (Date.now() - timestamp < CACHE_EXPIRY) {
      return photos;
    }
  }
  return {};
};

// Save photos to cache
const savePhotoCache = (photos) => {
  localStorage.setItem(
    PHOTO_CACHE_KEY,
    JSON.stringify({
      timestamp: Date.now(),
      photos,
    })
  );
};

// Fallback photo collections from Unsplash
const FALLBACK_PHOTOS = {
  male: [
    'https://images.unsplash.com/photo-1500648767791-00dcc994a43e',
    'https://images.unsplash.com/photo-1568602471122-7832951cc4c5',
    'https://images.unsplash.com/photo-1570295999919-56ceb5ecca61',
    'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d',
    'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d',
    'https://images.unsplash.com/photo-1519085360753-af0119f7cbe7',
    'https://images.unsplash.com/photo-1563351672-62b74891a28a',
    'https://images.unsplash.com/photo-1557862921-37829c790f19',
    'https://images.unsplash.com/photo-1564564321837-a57b7070ac4f',
    'https://images.unsplash.com/photo-1548372290-8d01b6c8e78c',
  ],
  female: [
    'https://images.unsplash.com/photo-1494790108377-be9c29b29330',
    'https://images.unsplash.com/photo-1438761681033-6461ffad8d80',
    'https://images.unsplash.com/photo-1544005313-94ddf0286df2',
    'https://images.unsplash.com/photo-1531123897727-8f129e1688ce',
    'https://images.unsplash.com/photo-1554151228-14d9def656e4',
    'https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e',
    'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2',
    'https://images.unsplash.com/photo-1487412720507-e7ab37603c6f',
    'https://images.unsplash.com/photo-1502823403499-6ccfcf4fb453',
    'https://images.unsplash.com/photo-1546961329-78bef0414d7c',
  ],
};

// Get a random photo from the collection
const getRandomPhoto = (collection) => {
  const index = Math.floor(Math.random() * collection.length);
  return collection[index];
};

// Get or generate a profile photo URL
export const getProfilePhoto = async (profileId, gender) => {
  const photoCache = getPhotoCache();
  
  // Return cached photo if exists
  if (photoCache[profileId]) {
    return photoCache[profileId];
  }

  // Use fallback photos if no API key or API fails
  const collection = gender.toLowerCase() === 'female' ? FALLBACK_PHOTOS.female : FALLBACK_PHOTOS.male;
  const photoUrl = getRandomPhoto(collection);

  // Cache the new photo
  photoCache[profileId] = photoUrl;
  savePhotoCache(photoCache);

  return photoUrl;
};

// Clear photo cache (call this when logging out)
export const clearPhotoCache = () => {
  localStorage.removeItem(PHOTO_CACHE_KEY);
}; 