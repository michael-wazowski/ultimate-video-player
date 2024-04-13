import { writeFileSync } from 'fs';
import { fail } from '@sveltejs/kit';

/** @type {import('./$types').Actions} */
export const actions = {
    default: async ({ request }) => {
      const formData = Object.fromEntries(await request.formData());

      if (
        !(formData.videoSelector as File).name ||
        (formData.videoSelector as File).name === 'undefined'
      ) {
        return fail(400, {
          error: true,
          message: 'You must provide a file to upload'
        });
      }
   
      const { videoSelector } = formData as { videoSelector: File };
  
      // Write the file to the static folder
      writeFileSync(`src/lib/assets/playedvideo.mp4`, Buffer.from(await videoSelector.arrayBuffer()));

      return {
        success: true
      };
    }
  };