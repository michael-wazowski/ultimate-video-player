<script>
    import Border from "./Border.svelte";
    import Grid from "./Grid.svelte";
    const BACKEND_URL = "http://127.0.0.1:8000";

    export let thumbNailUrl = "";
    export let title = "";
    export let id = 0;
    let lengthMinutes = 0.0;
    let duration = 0.0
    export let clickBinding;

    // We can get just a videos metadata with the video tag
    let metadataSource = BACKEND_URL + "/uploads/"  + id;

    function format(seconds) {
		if (isNaN(seconds)) return '...';

		const minutes = Math.floor(seconds / 60);
		seconds = Math.floor(seconds % 60);
		if (seconds < 10) seconds = '0' + seconds;

		return `${minutes}:${seconds}`;
	}

    $: lengthMinutes = format(duration);
</script>

<button on:click={clickBinding} style="flex: 0 1 300px ; align-self: flex-start; overflow-x: wrap; overflow-y: hidden;">
    <video style="display: none;" src="{metadataSource}" preload="metadata" bind:duration crossorigin="anonymous">
        <track kind="captions"/>
    </video>
    <Grid rows="1fr auto">
        <div style="width: 100%; height: 100%">
            <p>{lengthMinutes}</p>
            <img src={thumbNailUrl} alt="thumbnail">
        </div>

        <h3>
            {title}
        </h3>
    </Grid>
</button>

<style>
    button {
        transition: background-color 2s;
        background-color: #393939;
        border-color: transparent;
        border-radius: 15px;
        margin: 10px 5px 0px 5px;
    }

    div {
        position: relative;
    }

    img {
        margin: 15px 15px 0px 15px;
        width: calc(100% - 32px);
        height: calc(100% - 15px);
        border-radius: 15px;
    }

    p {
        position: absolute;
        right: 3rem;
        bottom: 10px;
        background-color: #262626;
        color: #f4f4f4;
        padding: 4px 8px 4px 8px;
        border-radius: 4px;
    }

    h3 {
        margin: 8px 15px 0px 15px;
        color: #f4f4f4;
        overflow-wrap: break-word;
        min-width: 0;
        text-align: start;
    }

    button div, button h3 {
        background-color: transparent;
    }

    button:hover{
        background-color: #606060;
        transition: background-color 0.8s;
    }
</style>