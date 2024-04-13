<script>
	import { writable, get } from 'svelte/store';

	import { exampleServerFunc } from "$lib/core/api";
    import VideoPlayer from "../lib/components/VideoPlayer.svelte";
	import Grid from "../lib/components/Grid.svelte";
	import Border from "../lib/components/Border.svelte";
	import Video from "$lib/assets/playedvideo.mp4"

   	let a = 0;
	let b = 0;
	let total = 0;
	
	let currentFile;
	let uploadForm;
	const videoShowing = writable(false);

	$: if(currentFile){
		videoShowing.set(true);
	}

	async function add() {
		total = await exampleServerFunc(a, b);
	}
</script>


<h1>
	Video Player Test
</h1>
{#if $videoShowing === true }
	<svelte:component this="{VideoPlayer}" fileSource="{Video}" thumbNailSource="https://sveltejs.github.io/assets/caminandes-llamigos.jpg"/>
{:else}
	<Grid rows="4rem calc(100% - 4rem)" columns="10% 80% 10%">
		<h3 style="grid-column: 2;">Please select a video file to play it back!</h3>

		<Border height="100%" width="100%" background="lightgray" corner="15px" style="grid-column: 2;">
			<form method="post" enctype="multipart/form-data" bind:this={uploadForm}>
				<input bind:value={currentFile} type="file" name="videoSelector" accept=".mp4"/>
			</form>
		</Border>
	</Grid>
{/if}
