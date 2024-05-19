<script>
    export let captions = [];
    export let currentTimeSeconds;
    export let maxTimeSeconds = 0;

    let container;
    let wait = false;

    $: handleTime(currentTimeSeconds);

    async function handleTime(t){
        if(!wait){
            wait = true;
            setTimeout(() => {wait = false; scrollToTarget();}, 1000); // Delay so that the DOM has time to update between scroll calls since time is updated way too quickly
        }
    }


    async function scrollToTarget(){
        await container?.scrollTo({top: container.scrollHeight*(currentTimeSeconds/maxTimeSeconds)-30, behavior: 'smooth'}); // -30 px for a slight delay since the user can read the top text already
    }
</script>

<div bind:this={container} class="hidden-scrollbar" style="width: 100%; height: 100%; overflow-y: scroll;">
{#each captions as cue, i}
<a href="" on:click={() => { currentTimeSeconds = cue.start}}><span id="{i}" class="inactive-cue" style="{(currentTimeSeconds >= cue.start && currentTimeSeconds < cue.end) ? "color: #f4f4f4" : "text-decoration: none;"}">{cue.content} </span></a>
{/each}
</div>

<style>
    .hidden-scrollbar::-webkit-scrollbar{
        display: none;
    }

    .hidden-scrollbar{
        -ms-overflow-style: none;  /* IE and Edge */
        scrollbar-width: none;  /* Firefox */
    }

    .active-cue {
        color: #f4f4f4;
    }

    .inactive-cue {
        color: gray;
    }

    span {
        font-family: Barlow;
    }

    span:hover{
        background-color: #606060;
        color: #f4f4f4;
    }

    a:hover {
        color: #f4f4f4;
    }

    a {
        text-decoration: none;
    }
</style>