<script>
    import Border from "./Border.svelte";
    import Grid from "./Grid.svelte";

    export let thumbNailUrl = "";
    export let title = "";
    export let length = 0.0;
    export let clickBinding;
</script>

<button on:click={clickBinding} style="flex: 1 1 0px ; align-self: flex-start; overflow-x: wrap;">
    <Grid rows="1fr 3rem">
        <div style="width: 100%; height: 100%">
            <p>{length}</p>
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
        margin: 10px;
    }

    div {
        position: relative;
    }

    img {
        margin: 15px 15px 15px 15px;
        width: calc(100% - 32px);
        height: calc(100% - 32px);
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
        color: #f4f4f4;
    }

    button div, button h3 {
        background-color: transparent;
    }

    button:hover{
        background-color: #606060;
        transition: background-color 0.8s;
    }
</style>