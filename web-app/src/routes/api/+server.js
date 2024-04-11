

import { json } from '@sveltejs/kit';
import pkg from 'node-calls-python';
const {nodecallspython} = pkg;

/**@type {import('./$types').RequestHandler} */export async function POST({ request }) {
  
  const py = nodecallspython.interpreter;

  py.import("./././././test/py").then(async function(pymodule) {
    const result = await py.call(pymodule, "add", 1, 2);
    console.log(result);
    return json(result);
  });
  const { a, b } = await request.json();
  return json(a + b);
}
