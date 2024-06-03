<script>
    import Border from "./Border.svelte";
    import Grid from "./Grid.svelte";
    import TrashSymbol from "$lib/assets/delete-icon.svg";
    import { formatToMins } from "$lib/core/formatting";
    const BACKEND_URL = "http://127.0.0.1:8000";

    export let thumbNailUrl = "";
    export let title = "";
    export let id = 0;
    export let status = 1;
    let lengthMinutes = 0.0;
    let duration = 0.0
    export let clickBinding;
    export let deleteHandler;

    // We can get just a videos metadata with the video tag
    let metadataSource = BACKEND_URL + "/uploads/" + id;

    $: lengthMinutes = formatToMins(duration);

    async function tryClick(e){
        if(status === 1){
            clickBinding(e);
        }
    }

</script>

<button on:click={tryClick} style="flex: 0 1 300px ; align-self: flex-start; overflow-x: wrap; overflow-y: hidden;" class="thumbnail-button">
    <video style="display: none;" src="{metadataSource}" preload="metadata" bind:duration crossorigin="anonymous">
        <track kind="captions"/>
    </video>
    <Grid rows="1fr auto">
        <div style="width: 100%; height: 100%">
            <p>{lengthMinutes}</p>
            <button on:click|stopPropagation={deleteHandler} class="delete-button">
                <img src={TrashSymbol} alt="Delete Video" class="delete-icon">
            </button>
            <img src={thumbNailUrl} alt="thumbnail" class="thumbnail">
            {#if status === 0}
                <div class="lds-spinner"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>
            {/if}
        </div>

        <h3>
            {title}
        </h3>
    </Grid>
</button>

<style>
    .thumbnail-button {
        transition: background-color 2s;
        background-color: #393939;
        border-color: transparent;
        border-radius: 15px;
        margin: 10px 5px 0px 5px;
    }

    div {
        position: relative;
        background-color: var(--based-color);
    }

    .thumbnail {
        margin: 15px 15px 0px 15px;
        width: calc(100% - 32px);
        height: calc(100% - 15px);
        border-radius: 15px;
    }

    .delete-button {
        position: absolute;
        right: 3rem;
        top: .9rem;
        display: none;
        background-color: transparent;
        border-style: none;
        z-index: 100;
        border-radius: 8px;
        transition: background-color 0.3s;
    }

    .delete-button:hover{
        background-color: #60606083;
        transition: background-color 0.3s;
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

    .thumbnail-button div, .thumbnail-button h3 {
        background-color: transparent;
    }

    .thumbnail-button:hover{
        background-color: #606060;
        transition: background-color 0.8s;
    }

    .thumbnail-button:hover .delete-button{
        display: block;
    }


    /* spinner */
    
        
    .lds-spinner,
    .lds-spinner div,
    .lds-spinner div:after {
        box-sizing: border-box;
        --currentColor: #f4f4f4;
    }
    .lds-spinner {
        color: var(--currentColor);
        display: inline-block;
        position: absolute;
        top: calc(50% - 40px);
        left: calc(50% - 40px);
        width: 80px;
        height: 80px;
    }
    .lds-spinner div {
        transform-origin: 40px 40px;
        animation: lds-spinner 1.2s linear infinite;
    }
    .lds-spinner div:after {
        content: " ";
        display: block;
        position: absolute;
        top: 3.2px;
        left: 36.8px;
        width: 6.4px;
        height: 17.6px;
        border-radius: 20%;
        background: var(--currentColor);
    }
    .lds-spinner div:nth-child(1) {
        transform: rotate(0deg);
        animation-delay: -1.1s;
    }
    .lds-spinner div:nth-child(2) {
        transform: rotate(30deg);
        animation-delay: -1s;
    }
    .lds-spinner div:nth-child(3) {
        transform: rotate(60deg);
        animation-delay: -0.9s;
    }
    .lds-spinner div:nth-child(4) {
        transform: rotate(90deg);
        animation-delay: -0.8s;
    }
    .lds-spinner div:nth-child(5) {
        transform: rotate(120deg);
        animation-delay: -0.7s;
    }
    .lds-spinner div:nth-child(6) {
        transform: rotate(150deg);
        animation-delay: -0.6s;
    }
    .lds-spinner div:nth-child(7) {
        transform: rotate(180deg);
        animation-delay: -0.5s;
    }
    .lds-spinner div:nth-child(8) {
        transform: rotate(210deg);
        animation-delay: -0.4s;
    }
    .lds-spinner div:nth-child(9) {
        transform: rotate(240deg);
        animation-delay: -0.3s;
    }
    .lds-spinner div:nth-child(10) {
        transform: rotate(270deg);
        animation-delay: -0.2s;
    }
    .lds-spinner div:nth-child(11) {
        transform: rotate(300deg);
        animation-delay: -0.1s;
    }
    .lds-spinner div:nth-child(12) {
        transform: rotate(330deg);
        animation-delay: 0s;
    }
    @keyframes lds-spinner {
    0% {
        opacity: 1;
    }
    100% {
        opacity: 0;
    }
    }
</style>