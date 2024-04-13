<script>
	import { writable, get } from 'svelte/store';
	import { Guid } from "js-guid";
	
	import { exampleServerFunc, getVideos, getVideoFileUrl } from "$lib/core/api";
    import VideoPlayer from "../lib/components/VideoPlayer.svelte";
	import Grid from "../lib/components/Grid.svelte";
	import Border from "../lib/components/Border.svelte";
	import Video from "$lib/assets/playedvideo.mp4"

   	let a = 0;
	let b = 0;
	let total = 0;
	let promise = queryVideos();
	let dynamicVideo = null;

	let currentFile;
	let uploadForm;
	const videoShowing = writable(false);

	$: if(currentFile){
		videoShowing.set(true);
	}

	async function add() {
		total = await exampleServerFunc(a, b);
	}

	async function queryVideos() {
		return await getVideos();
	}

	async function onSelectVideo(id = 0){
		let response = await getVideoFileUrl(id);
		if(response != null){
			let absoluteUrl = "http://127.0.0.1:8000" + response;
			console.log(absoluteUrl);
			dynamicVideo = absoluteUrl;
			videoShowing.set(true);
		}
	}
</script>


<h1>
	Video Player Test
</h1>
{#if $videoShowing === true }
	<svelte:component this="{VideoPlayer}" fileSource="{dynamicVideo === null ? Video : dynamicVideo}" thumbNailSource="https://sveltejs.github.io/assets/caminandes-llamigos.jpg"/>
{:else}
	<Grid rows="4rem 20rem 4rem 1fr" columns="10% 80% 10%">
		<h3 style="grid-column: 2;">Please select a video file to play it back!</h3>

		<Border height="100%" width="100%" background="lightgray" corner="15px" style="grid-column: 2;">
			<form method="post" enctype="multipart/form-data" bind:this={uploadForm}>
				<input bind:value={currentFile} type="file" name="videoSelector" accept=".mp4"/>
			</form>
		</Border>

		<h3 style="grid-column: 2;"> Or select an existing video to watch it again!</h3>

		<Border height="100%" width="100%" background="lightgray" corner="15px" style="grid-column: 2;">
			{#await promise}
				<h2> Loading vids</h2>
			{:then videos}
				<ul>
					{#each videos as { filename, id }, i}
						<li>
							<button on:click={() => onSelectVideo(id)}>
								{filename}
							</button>
						</li>		
					{/each}
				</ul>
			{/await}
		</Border>
	</Grid>
{/if}
