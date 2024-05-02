
import { json, fail } from '@sveltejs/kit';


// Example function for server side code execution
/**@type {import('./$types').RequestHandler} */export async function POST({ request }) {
  
  const { a, b } = await request.json();
  return json(a + b);
}
