<script>
    export let captions = [];
    export let currentTimeSeconds;
    export let currentCueStartTime; // Binding to the cue currently shown by the video player

    let filteredCaptions = captions;

    let container;
    let wait = false;

    $: handleTime(currentTimeSeconds);

    async function handleTime(t){
        if(!wait){
            wait = true;
            setTimeout(() => {wait = false; scrollToTarget();}, 1000); // Delay so that the DOM has time to update between scroll calls since time is updated way too quickly
        }
    }


    async function getTargetOffset(startTime){
        if(startTime){
            return document.getElementById(startTime)?.offsetTop;
        }

        return 0;
    }

    async function scrollToTarget(){
        await container?.scrollTo({top:  (await getTargetOffset(currentCueStartTime))-(container.clientHeight/2), behavior: 'smooth'}); // - containerheight / 2 to try and always center current caption
    }

    let searchTerm = "";
	// resets language menu if search input is used
	
	const searchCues = () => {	
		return filteredCaptions = captions.filter(cue => {
			let cueText = cue.content.toLowerCase();
			return cueText.includes(searchTerm.toLowerCase())
		});
	}
</script>
<div id="capt-container">
<div id="search-input-cont">
    <input type="text" 
                 id="search-field" 
                 placeholder="Enter Search Term" 
                 autocomplete="off"
                 bind:value={searchTerm}
                 on:input|stopPropagation={searchCues} />
</div> 
<div bind:this={container} class="hidden-scrollbar" style="overflow-y: scroll;">
    
{#each filteredCaptions as cue, i}
<a href="" on:click={() => { currentTimeSeconds = cue.start}}><span id="{cue.start}" class="inactive-cue" style="{((currentTimeSeconds >= cue.start && currentTimeSeconds < cue.end) || searchTerm != "") ? "color: #f4f4f4" : "text-decoration: none;"}">{cue.content} </span></a>
{#if searchTerm != ""}
<br><br>
{/if}
{/each}
</div>
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

    #search-input-cont {
		width: 80%;
		display: flex;
        margin-bottom: 10px;
	}

	#search-field {
		width: 100%;
		font-size: 1rem;
		border: 1px solid gray;
		border-radius: 5px;
		padding: 8px;
	}

    #capt-container {
        display: flex;
        flex-direction: column;
        height: 10%;

        background-color: #393939; 
        padding: 1rem; 
        border-radius: 8px;

        flex-basis: 50%;
        flex-grow: 1;
        flex-shrink: 1;
    }
</style>