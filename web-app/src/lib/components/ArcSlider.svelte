<script>
	import { tweened } from "svelte/motion";
	import { pannable } from "../core/pannable";
	import { formatToMins } from "$lib/core/formatting";

	let trackColor = "";
	let thumbColor = "";
	let thumbWidth = 5;
	let thumbHeight = 25;

	export let time;
	export let captionTrack;
	export let duration;

	//all of the events from the captions marked with "IP" (interest point)
	let sliderEvents = [];

	//all of the events from slider events currently visible
	let visibleSliderEvents = [];
	//let visibleSliderEvents = [{content: "Text",time: 10},{content: "Text2", time: 30},{content: "Text3", time: 60},{content: "Text4", time: 120}];
	//let visibleSliderEvents = [{content: "Text2", angle: 25.8419, time: 120}];

	function handlePanStart() {
		//update the mouse cursor css
	}

	function handlePanMove(event) {
		//what is the new time going to be
		//minus because the mouse moves left = time goes forward
		//division by 300 just a rough estimate, mouse movement feels pretty 1:1 with the resulting rotation
		let proposedTime = time - event.detail.dx * ($currentTimeScale / 300);

		//dont run off the end of the video
		if (proposedTime < 0) {
			proposedTime = 0;
		} else if (proposedTime > duration) {
			proposedTime = duration;
		}

		//update the actual time
		time = proposedTime;
	}

	function handlePanEnd(event) {
		//update the mouse cursor css
	}

	//When time changes, figure out the state of our chips
	$: handleTime(time);

	//Force it to change when page loads (this relies on captionTrack loading fast)
	setTimeout(() => {
		sliderEvents = []
		handleTime(time);
	}, 100);

	let processed = false;

	let sliderLI = 0; //slider event search index
	let sliderRI = 0;

	let zoomThresh = 0; //trying to stop quick snaps

	async function handleTime(timeV) {
		//pull all of the cues into an array (the cue list isn't actually an array)
		if (sliderEvents.length == 0 && !processed) {
			processCaptionTrack();
			console.log("Process caption track");
		} else {
			processed = true;
		}

		//look at the oldest / newest time, is it still within timescale
		//if not, remove it
		if (visibleSliderEvents.length > 0) {
			while (visibleSliderEvents[0].time < timeV - $currentTimeScale) {
				console.log("late");
				visibleSliderEvents = visibleSliderEvents.slice(1);
				sliderLI++;
				console.log("sliderLI", sliderLI);
			}

			while (visibleSliderEvents[visibleSliderEvents.length-1].time > timeV + $currentTimeScale + $currentTimeScale) {
				console.log("early");
				visibleSliderEvents = visibleSliderEvents.slice(0,-2);
				sliderRI--;
				console.log("sliderRI", sliderRI);
			}
		}

		// //if we dont have enough events on the slider, get more
		// if (sliderEvents.length > 1) { //visibleSliderEvents.length < 3 &&
		// 	//i dont like this line of code
		// 	while (sliderEvents[0].time < timeV + $currentTimeScale) {
		// 		visibleSliderEvents.push(sliderEvents[0]);

		// 		sliderEvents = sliderEvents.slice(1);

		// 		//console.log(visibleSliderEvents, sliderEvents);
		// 	}
		// }

		//if there are 2 events or more
		if (sliderEvents.length > 1) {

			//dont go off the end of the array
			if (sliderRI < sliderEvents.length){

				//expand the visible slider events slice to be all events within timescale
				while (sliderEvents[sliderRI].time < timeV + $currentTimeScale) {

					//somehow check if the next event is too close to the previous one and don't add it until the timescale adjustment wont force it out
					
					sliderRI++;
					visibleSliderEvents = sliderEvents.slice(sliderLI,sliderRI);
					
					console.log("SliderRI", sliderRI);

					if(sliderRI == sliderEvents.length){
						break;
					}

				}
			}

			//dont go off the end of the array
			if (sliderLI > 0) {
				//expand the visible slider events slice to be all events within timescale
				while (sliderEvents[sliderLI-1].time > timeV - $currentTimeScale) {

					sliderLI--;
					visibleSliderEvents = sliderEvents.slice(sliderLI,sliderRI);
					
					console.log("SliderLI", sliderLI);

					if(sliderLI == 0){
						break;
					}
				}
			}
			//console.log(visibleSliderEvents,sliderLI,sliderRI)
		}

		// if (visibleSliderEvents.length > 0 && sliderEvents.length > 0) {
		// 	//if the there are no events on the right of the slider
		// 	if (
		// 		visibleSliderEvents[visibleSliderEvents.length - 1].time < timeV
		// 	) {
		// 		console.log("Nothing On RHS, pulling new Chip");
		// 		$currentTimeScale = sliderEvents[0].time - timeV;
		// 		visibleSliderEvents.push(sliderEvents[0]);
		// 		sliderEvents = sliderEvents.slice(1);
		// 	}
		// }

		if (visibleSliderEvents.length > 0 && sliderEvents.length > 0) {
			//if the there are no events on the right of the slider
			if (
				visibleSliderEvents[visibleSliderEvents.length - 1].time < timeV
			) {
				if (sliderRI + 1 < sliderEvents.length){
					console.log("Nothing On RHS, pulling new Chip");
					//visibleSliderEvents.push(sliderEvents[sliderRI]);

					sliderRI++;
					visibleSliderEvents = sliderEvents.slice(sliderLI,sliderRI);

					//$currentTimeScale = sliderEvents[sliderRI].time - timeV;

					console.log("SliderRI", sliderRI);

				}
			}
		}

		//find the smallest difference between two chips and adjust timescale so they dont overlap
		if (visibleSliderEvents.length >= 2) {
			let smallestPDelta = 100;
			let T1 = null;
			let T2 = null;

			for (let index = 1; index < visibleSliderEvents.length; index++) {

				//times
				const eventTime = visibleSliderEvents[index].time;
				const previousEventTime = visibleSliderEvents[index - 1].time;

				//percentage of each time between current and current + timescale
				let percentage = (eventTime - time) / $currentTimeScale;
				let previousPercentage = (previousEventTime - time) / $currentTimeScale;

				//difference in percentage between the 2 times
				let PDelta = percentage - previousPercentage;

				//what would happen if we zoomed in
				let potentialTimeScale = ((eventTime-time)-(previousEventTime-time))/0.24
				let potentialPercentage = (eventTime - time) / potentialTimeScale;
				let potentialPercentage2 = (previousEventTime - time) / potentialTimeScale;

				//would the zoom be outside of scale / or be happening on the left side of the slider
				if (potentialPercentage > 1 || potentialPercentage2 > 1 || (percentage < 0 && previousPercentage < 0)){
					//console.log(potentialPercentage);
				}else {
					//if valid zoom
					if (PDelta < smallestPDelta) {
						smallestPDelta = PDelta;
						T2 = eventTime;
						T1 = previousEventTime;
					}
				}
			}

			smallestPDelta = Math.round(smallestPDelta * 100000) / 100000;

			//todo, add some kind of check for if this will shove the things out of view
			if (zoomThresh <= 0 && T1 != null && T2 != null){
				if (smallestPDelta < 0.23) {
					$currentTimeScale = ((T2-time)-(T1-time))/0.24
					console.log(smallestPDelta, $currentTimeScale, "zoom in")
					zoomThresh = 10;
				} else if (smallestPDelta > 0.5) {
					$currentTimeScale = ((T2 - time) - (T1 - time)) / 0.5;
					console.log(smallestPDelta, $currentTimeScale, "zoom out");
					zoomThresh = 10;
				}
			} else {
				console.log(zoomThresh);
				zoomThresh--;
			}
		}
	}

	//get each of the cues from captionTrack with id = "IP"
	function processCaptionTrack() {
		sliderEvents = [];
		if (typeof captionTrack != "undefined") {
			let cues = captionTrack.track.cues;

			for (let index = 0; index < cues.length; index++) {
				const cue = cues[index];

				if (cue.id == "IP") {
					sliderEvents.push({
						content: cue.text,
						time: cue.startTime,
					});
				}
			}

			if (sliderEvents.length != 0){
				sliderEvents.push({
						content: "End of Content",
						time: duration,
				});
			}	
		}
	}

	//delta between current timestamp and most forward point on the graph
	let currentTimeScale = tweened(60, { duration: 500 });

	//want to restructure the divs so this doesn't need to be estimated
	//let y = 0.9
	//let x=Math.sqrt(1-(y*y))
	let endAngle = 35; //90 - (Math.atan(y/x) * 180 / Math.PI);

	//haven't got dynamic timescale happening yet
	function handleClick() {
		//sets the target to tween() towards
		$currentTimeScale = 240;
	}
</script>

<div class="container" >
	<div
		use:pannable
		on:panstart={handlePanStart}
		on:panmove={handlePanMove}
		on:panend={handlePanEnd}
		class="elipse-path"
		id="elipsePath"
		style="border-color:{trackColor};"
	></div>

	<div class="rotator" style="border-color:{trackColor};">
		<div
			class="box"
			style="transform:
			translate(0px,-15px); background-color:{thumbColor}; --width:{thumbWidth}px; --height:{thumbHeight}px;"
		>
			<div class="boxText">
				<br /><br /><br />
				{formatToMins(time)}
			</div>
		</div>
	</div>

	{#each visibleSliderEvents as chip}
		<div
			class="rotator"
			style="rotate: {((chip.time - time) / $currentTimeScale) *
				endAngle}deg ; border-color:{trackColor};"
		>
			<div
				class="box"
				style="transform: translate(0px,-15px); background-color:{thumbColor}; --width:{thumbWidth}px; --height:{thumbHeight}px;"
			>
				<div class="boxText">
					{formatToMins(chip.time)}
					<br />
					{chip.content.slice(0, 20)}
				</div>
			</div>
		</div>
	{/each}
</div>

<button on:click={handleClick} style="transform-origin: 0 0">
	test button changes timescale
</button>

<style>
	* {
		--track-width: 4px;
	}

	.box {
		--width: 15px;
		--height: 25px;
		position: absolute;
		width: var(--width);
		height: var(--height);
		left: calc(50% - var(--width) / 2);
		border-radius: calc(var(--width) / 2);
		background-color: #0f62fe;
		cursor: move;
		color: white;
	}

	.boxText {
		width: 80px;
		text-align: center;
		position: absolute;
		left: 50%;
		top: 50%;
		transform: translate(-50%, 25%);
		font-size: 15px;
		font-family: Barlow;
	}

	.elipse-path {
		background-color: transparent;
		border-width: var(--track-width);
		border-color: white;
		border-style: solid;
		border-radius: 50%;
		position: absolute;
		height: auto;

		clip-path: inset(0px 0px 90%);

		width: 100%;
		aspect-ratio: 1 / 1;

		cursor: grab;
		/* todo make this change on click */
	}

	.rotator {
		background-color: transparent;
		width: 100%;
		border-width: var(--track-width);
		border-color: rgba(255, 255, 255, 0);
		border-style: solid;
		position: absolute;
		aspect-ratio: 1 / 1;
		pointer-events: none;
	}

	.container {
		padding-top: 11px;

		aspect-ratio: 9 / 1;

		width: 100%;

		overflow: hidden;
	}
</style>
