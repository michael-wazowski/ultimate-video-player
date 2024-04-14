<script>
	import { writable, get } from 'svelte/store';
	import { Guid } from "js-guid";
	
	import { exampleServerFunc, getVideos, getVideoFileUrl } from "$lib/core/api";
    import VideoPlayer from "../lib/components/VideoPlayer.svelte";
	import Grid from "../lib/components/Grid.svelte";
	import Border from "../lib/components/Border.svelte";
	import VideoThumbnail from '../lib/components/VideoThumbnail.svelte';
	import Video from "$lib/assets/playedvideo.mp4"
	import PlusSymbol from "$lib/assets/plus-symbol.svg"

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
	Ultimate Video Player
</h1>
{#if $videoShowing === true }
	<svelte:component this="{VideoPlayer}" fileSource="{dynamicVideo === null ? Video : dynamicVideo}" thumbNailSource="https://sveltejs.github.io/assets/caminandes-llamigos.jpg"/>
{:else}
	<Grid rows="4rem 20rem 4rem 1fr" columns="10% 80% 10%">
		<h3 style="grid-column: 2;">Please select a video file to play it back!</h3>

		<Border height="100%" width="100%" style="grid-column: 2;">
			<form method="post" enctype="multipart/form-data" bind:this={uploadForm} style="height: 100%; width: 100%;">
				<label for="file-upload" class="custom-file-area">
					<Grid columns="1fr 1fr 1fr" rows="1fr 1fr 1fr">
						<img src="{PlusSymbol}" alt="upload file here" style="width: 100px; height: auto; grid-row: 2; grid-column: 2; margin: auto; background-color: transparent;"/>
					</Grid>
					<input bind:value={currentFile} type="file" name="videoSelector" accept=".mp4" class="file-area" id="file-upload"/>
				</label>
			</form>
		</Border>

		<h3 style="grid-column: 2;"> Or select an existing video to watch it again!</h3>

		<Border height="100%" width="100%" corner="15px" style="grid-column: 2; overflow-y: scroll; overflow-x: hidden;">
			{#await promise}
				<h2> Loading vids</h2>
			{:then videos}
				<div class="uploaded-list-container" style="display: flex; flex-wrap: wrap;">
					{#each videos as { filename, id }, i}
						<VideoThumbnail clickBinding={() => onSelectVideo(id)} thumbNailUrl="https://picsum.photos/600/300" title={filename} length=12.2 />
					{/each}
				</div>
			{/await}
		</Border>
	</Grid>
{/if}


<style>
	@font-face {
		font-family: Barlow;
		src: url("$lib/assets/Barlow-Regular.ttf");
	}

	*, html * {
		font-family: Barlow;
		background-color: #262626;
		color: #f4f4f4;
	}


	.file-area{
		width: 100%;
		height: 100%;
		opacity: 0;
		cursor: pointer;
		position: absolute;
		left: 0;
		top: 0;
		bottom: 0;
	}

	.custom-file-area{
		width: 100%;
		height: 100%;
		background-color: #393939;
		border-radius: 15px;
		display: inline-block;
  		position: relative;
		cursor: pointer;
		transition: background-color 0.8s;
	}

	.custom-file-area:hover{
		background-color: #606060;
		transition: background-color 0.8s;
	}

	.uploaded-list-container{
		width: 100%;
		height: 100%;
		list-style-type: none;
	}

	.uploaded-list-item{
		background-color: #6f6f6f;
		margin-top: 10px;
	}

	.uploaded-list-item button{
		background-color: transparent;
		color: #ffffff;
		border-style: none;
	}

	.uploaded-list-item:hover{
		background-color: #606060;
	}



</style>