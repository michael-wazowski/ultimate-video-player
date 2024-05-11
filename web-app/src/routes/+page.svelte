<script>
	import { writable, get } from 'svelte/store';
	import { Guid } from "js-guid";
	
	import { getVideos } from "$lib/core/api";
    import VideoPlayer from "../lib/components/VideoPlayer.svelte";
	import Grid from "../lib/components/Grid.svelte";
	import Border from "../lib/components/Border.svelte";
	import VideoThumbnail from '../lib/components/VideoThumbnail.svelte';

	import PlusSymbol from "$lib/assets/plus-symbol.svg";

	// Used to start preloading the list of videos the user has
	let promise = queryVideos();
	
	let form;
	let dynamicVideo = null;
	let blockUpload = false;

	let currentFile;
	const videoShowing = writable(false);
	const BACKEND_URL = "http://127.0.0.1:8000"; //"https://carbonlaptop.tail0a458.ts.net:10000"

	// This if statement is run each time the currentfile variable is changed (as a result of the $: )
	$: if(currentFile && blockUpload == false){
		form.requestSubmit();
		if(dynamicVideo != null){
			videoShowing.set(true);
		}
		
		//form.requestSubmit();
	}

	// Querys the python server from the client side, returns the list of videos the client has
	async function queryVideos() {
		return await getVideos(BACKEND_URL);
	}

	// Callback that takes a videos id, gets the filename and then changes the video player source to the url for the video
	async function onSelectVideo(id = 0){
		// gets the static sub url of the video
		//let response = await getVideoFileUrl(id);
		//if(response != null){
			// Video urls are currently static and just a combination of the video id and its filename
		let absoluteUrl = BACKEND_URL + "/uploads/"+id;

		dynamicVideo = absoluteUrl;
		videoShowing.set(true);
		//}
	}

	async function handleVideoUpload(event){
		blockUpload = true;
		var formData = new FormData();
		formData.append("file", currentFile.item(0));

		let response = await fetch(BACKEND_URL + "/", {
      		method: "POST",
      		body: formData,
			redirect: 'follow'
   		});

		let subUrl = await response.text();
		let absoluteUrl = BACKEND_URL + subUrl;

		dynamicVideo = absoluteUrl;
		videoShowing.set(true);
	}
</script>


<h1>
	<a on:click={()=>videoShowing.set(false)} href="/">Ultimate Video Player</a>
</h1>
{#if $videoShowing === true }
	<svelte:component this="{VideoPlayer}" fileSource={dynamicVideo}/>
{:else}
	<Grid rows="4rem 20rem 4rem 1fr" columns="10% 80% 10%">
		<h3 style="grid-column: 2;">Please select a video file to play it back!</h3>

		<Border height="100%" width="100%" style="grid-column: 2;">
			<form method="post" enctype="multipart/form-data" style="height: 100%; width: 100%;" on:submit|preventDefault={handleVideoUpload} bind:this={form}>
				<label for="file-upload" class="custom-file-area">
					<Grid columns="1fr 1fr 1fr" rows="1fr 1fr 1fr">
						<img src="{PlusSymbol}" alt="upload file here" style="width: 100px; height: auto; grid-row: 2; grid-column: 2; margin: auto; background-color: transparent;"/>
					</Grid>
					<input bind:files={currentFile} type="file" name="videoSelector" accept=".mp4" class="file-area" id="file-upload"/>
					<input type="submit" style="display: none;">
				</label>
			</form>
		</Border>

		<h3 style="grid-column: 2;"> Or select an existing video to watch it again!</h3>

		<Border height="100%" width="100%" corner="15px" style="grid-column: 2; overflow-y: scroll; overflow-x: hidden; height: 600px">
			{#await promise}
				<h2> Loading vids</h2>
			{:then videos}
				<div class="uploaded-list-container" style="display: flex; flex-wrap: wrap;">
					{#each videos as { filename, id }, i}
						<VideoThumbnail clickBinding={() => onSelectVideo(id)} thumbNailUrl="{BACKEND_URL}/uploads/{id}/thumb" title={filename} length=12.2 />
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

	h1 > a{
		text-decoration: none;
	}



</style>