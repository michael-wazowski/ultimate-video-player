<script>
	import { exampleServerFunc } from "$lib/core/api"
   	let a = 0;
	let b = 0;
	let total = 0;
 
	async function add() {
		total = await exampleServerFunc(a, b);
	}
</script>


<input type="number" bind:value={a}> +
<input type="number" bind:value={b}> =
{total}

<button on:click={add}>Calculate</button>