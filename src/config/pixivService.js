// src/services/pixivService.js
import axios from 'axios';

const PIXIV_API_URL = 'https://pixiv.mokeyjay.com/?r=api/pixiv-json';

export const getPixivDailyRanking = async () => {
  try {
    const response = await axios.get(PIXIV_API_URL);
    console.log('Pixiv API response:', response.data); // 添加日志
    return response.data;
  } catch (error) {
    console.error('Error fetching Pixiv daily ranking:', error);
    throw error;
  }
};

