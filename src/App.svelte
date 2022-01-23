<script>
    let mode = 0;
    window.onload = () => {
        LoadKanjiFromLocalStorage()
        AddAllHiragana()
        AddAllKatakana()
    }
    let kanjiLists = {
        "1": [],
        "2": [],
        "3": [],
        "4": [],
        "5": [],
        "6": [],
        "S": [],
    };

    function shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
    }

    let kanjiTrainObject;



    let selectedMeaning = "";
    let selectedPronounciation = "";
    let combo = 0;
    function OnAddKanji(level) {
        fetch("kanjiGrade"+level+".csv").then(res => res.text().then(text => {
            let lines = text.split('\n')
            let headers = lines[0].split(",");

            const kanjiLength = kanjiLists[level].length

            for (let i = 1; i<lines.length; i++) {
                let obj = {}
                let currentLine = lines[i].split(",")
                for (let j = 0; j < headers.length; j++) {
                    obj[headers[j]] = currentLine[j]
                }
                if (i-1 === kanjiLength) {
                    if (window.confirm("The kanji is: " + TextFromKanjiObject(obj) + ". Would you like to add to databank?")) {
                        AddKanjiToLocalStorage(level, obj)
                    }

                }
            }
        }))
    }

    function TextFromKanjiObject(kanjiObject) {
        return kanjiObject["New (Shinjitai)"] + " - " + kanjiObject["English meaning"] + " - " + kanjiObject["Readings"]
    }

    function LoadKanjiFromLocalStorage() {
        let kanjiStorage = JSON.parse(localStorage.getItem("KanjiStorage"))
        if (kanjiStorage == null) {
            kanjiStorage = {
                "1": [],
                "2": [],
                "3": [],
                "4": [],
                "5": [],
                "6": [],
                "S": [],
            };
        }
        kanjiLists = kanjiStorage

        if (Object.values(kanjiLists).some(list => list.length !== 0)) {
            LoadRandomKanji()
        }
    }

    function AddKanjiToLocalStorage(level, kanjiObject) {
        let kanjiStorage = JSON.parse(localStorage.getItem("KanjiStorage"))
        if (kanjiStorage == null) {
            kanjiStorage = {
                "1": [],
                "2": [],
                "3": [],
                "4": [],
                "5": [],
                "6": [],
                "S": [],
            };
        }
        kanjiStorage[level] = [...kanjiStorage[level], kanjiObject]
        kanjiLists = kanjiStorage
        localStorage.setItem("KanjiStorage", JSON.stringify(kanjiStorage))
        LoadRandomKanji()
    }

    function ResetDatabase() {
        kanjiLists = {
            "1": [],
            "2": [],
            "3": [],
            "4": [],
            "5": [],
            "6": [],
            "S": [],
        };
        localStorage.setItem("KanjiStorage", JSON.stringify(kanjiLists))
        LoadRandomKanji()
    }

    let listClosed = true

    function OpenList() {
        listClosed = !listClosed;

        if (listClosed) {

        } else {

        }
    }

    function LoadRandomKanji() {
        let allKanji = []
        Object.values(kanjiLists).forEach(list => allKanji = [...allKanji, ...list])
        let index = Math.floor(Math.random() * (allKanji.length))

        let englishOptions = []
        let englishIndex = index
        while (englishOptions.length < Math.min(6, allKanji.length)) {
            let englishMeaning = allKanji[englishIndex]["English meaning"];
            if (!englishOptions.some(option => option["value"] === englishMeaning)) {
                englishOptions.push({"value": englishMeaning, "selected": false})
            }
            englishIndex = Math.floor(Math.random() * (allKanji.length))
        }

        let japaneseOptions = []
        let japaneseIndex = index
        while (japaneseOptions.length < Math.min(6, allKanji.length)) {
            let japaneseMeaning = allKanji[japaneseIndex]["Readings"];

            if (!japaneseOptions.some(option => option["value"] === japaneseMeaning)) {
                japaneseOptions.push({"value": japaneseMeaning, "selected": false})
            }
            japaneseIndex = Math.floor(Math.random() * (allKanji.length))
        }

        shuffleArray(englishOptions)
        shuffleArray(japaneseOptions)

        kanjiTrainObject = {
            "kanji": allKanji[index],
            "englishOptions": englishOptions,
            "japaneseOptions": japaneseOptions
        }
    }


    function SelectMeaning(e) {
        let meaning = e.target.innerText
        selectedMeaning = meaning
        kanjiTrainObject.englishOptions.forEach(option => {
            option["selected"] = option["value"] === meaning
        })
        // noinspection SillyAssignmentJS
        kanjiTrainObject = kanjiTrainObject

        if (selectedMeaning !== "" && selectedPronounciation !== "") {
            setTimeout(GuessKanji, 250)
        }
    }


    function SelectPronounciation(e) {
        let pronounciation = e.target.innerText
        selectedPronounciation = pronounciation
        kanjiTrainObject.japaneseOptions.forEach(option => {
            option["selected"] = option["value"] === pronounciation
        })
        // noinspection SillyAssignmentJS
        kanjiTrainObject = kanjiTrainObject

        if (selectedMeaning !== "" && selectedPronounciation !== "") {
            setTimeout(GuessKanji, 250)
        }
    }

    function GuessKanji() {
        if (kanjiTrainObject.kanji["English meaning"] === selectedMeaning && kanjiTrainObject.kanji["Readings"] === selectedPronounciation) {
            combo++
        } else {
            combo = 0
        }
        selectedPronounciation = ""
        selectedMeaning = ""
        LoadRandomKanji()
    }


    // Hiragana code
    let hiraganaTrainObject
    let hiraganaList = []
    let selectedHiragana = ""
    function AddAllHiragana() {
        fetch("Hiragana.csv").then(res => res.text().then(text => {
            let lines = text.split('\n')
            let headers = lines[0].split(",");

            for (let i = 1; i<lines.length; i++) {
                let obj = {}
                let currentLine = lines[i].split(",")
                for (let j = 0; j < headers.length; j++) {
                    obj[headers[j]] = currentLine[j]
                }
                hiraganaList = [...hiraganaList, obj]
            }
            LoadRandomHira()
        }))
    }

    function LoadRandomHira() {
        let index = Math.floor(Math.random() * (hiraganaList.length))

        let readings = []
        let readingIndex = index
        while (readings.length < Math.min(6, hiraganaList.length)) {
            let englishMeaning = hiraganaList[readingIndex]["Readings"];
            if (!readings.some(option => option["value"] === englishMeaning)) {
                readings.push({"value": englishMeaning, "selected": false})
            }
            readingIndex = Math.floor(Math.random() * (hiraganaList.length))
        }

        shuffleArray(readings)

        hiraganaTrainObject = {
            "Hiragana": hiraganaList[index],
            "Readings": readings,
        }
    }

    function GuessHiragana() {
        if (hiraganaTrainObject.Hiragana["Readings"] === selectedHiragana) {
            combo++
        } else {
            combo = 0
        }
        selectedHiragana = ""
        LoadRandomHira()
    }

    function SelectHiragana(e) {
        let hiragana = e.target.innerText
        selectedHiragana = hiragana
        hiraganaTrainObject.Readings.forEach(option => {
            option["selected"] = option["value"] === hiragana
        })
        // noinspection SillyAssignmentJS
        hiraganaTrainObject = hiraganaTrainObject

        if (selectedHiragana !== "") {
            setTimeout(GuessHiragana, 250)
        }
    }

    let katakanaTrainObject
    let katakanaList = []
    let selectedKatakana = ""
    function AddAllKatakana() {
        fetch("Katakana.csv").then(res => res.text().then(text => {
            let lines = text.split('\n')
            let headers = lines[0].split(",");

            for (let i = 1; i<lines.length; i++) {
                let obj = {}
                let currentLine = lines[i].split(",")
                for (let j = 0; j < headers.length; j++) {
                    obj[headers[j]] = currentLine[j]
                }
                katakanaList = [...katakanaList, obj]
            }
            LoadRandomKata()
        }))
    }


    function LoadRandomKata() {
        let index = Math.floor(Math.random() * (katakanaList.length))

        let readings = []
        let readingIndex = index
        while (readings.length < Math.min(6, katakanaList.length)) {
            let englishMeaning = katakanaList[readingIndex]["Readings"];
            if (!readings.some(option => option["value"] === englishMeaning)) {
                readings.push({"value": englishMeaning, "selected": false})
            }
            readingIndex = Math.floor(Math.random() * (katakanaList.length))
        }

        shuffleArray(readings)

        katakanaTrainObject = {
            "Katakana": katakanaList[index],
            "Readings": readings,
        }
    }


    function SelectKatakana(e) {
        let katakana = e.target.innerText
        selectedKatakana = katakana
        katakanaTrainObject.Readings.forEach(option => {
            option["selected"] = option["value"] === katakana
        })
        // noinspection SillyAssignmentJS
        katakanaTrainObject = katakanaTrainObject

        if (selectedKatakana !== "") {
            setTimeout(GuessKatakana, 250)
        }
    }


    function GuessKatakana() {
        if (katakanaTrainObject.Katakana["Readings"] === selectedKatakana) {
            combo++
        } else {
            combo = 0
        }
        selectedKatakana = ""
        LoadRandomKata()
    }

    function TextGuessKata(e) {
        if (!manualEnter) {
            if (e.target.value + e.code.replace("Key", "").toLowerCase() === katakanaTrainObject.Katakana["Readings"].replace("(", "").replace(")", "")) {
                e.preventDefault()
                combo++
                selectedKatakana = ""
                e.target.value = ""
                LoadRandomKata()
            }
        }
        if (e.code === "Space") {
            if (e.target.value === katakanaTrainObject.Katakana["Readings"].replace("(", "").replace(")", "")) {
                combo++
            } else {
                combo = 0
            }
            e.preventDefault()
            selectedKatakana = ""
            e.target.value = ""
            LoadRandomKata()
        }
    }

    function TextGuessHira(e) {
        if (!manualEnter) {
            if (e.target.value + e.code.replace("Key", "").toLowerCase() === hiraganaTrainObject.Hiragana["Readings"].replace("(", "").replace(")", "")) {
                e.preventDefault()
                combo++
                selectedHiragana = ""
                e.target.value = ""
                LoadRandomHira()
            }
        }
        if (e.code === "Space") {
            if (e.target.value === hiraganaTrainObject.Hiragana["Readings"].replace("(", "").replace(")", "")) {
                combo++
            } else {
                combo = 0
            }

            e.preventDefault()
            selectedHiragana = ""
            e.target.value = ""
            LoadRandomHira()
        }
    }

    let manualEnter = false

</script>
<style>
    main {
        width: 100%;
        height: 100%;
    }

    .main-box {
        width: 100%;
        height: calc(100% - 100px);
        display: flex;
        overflow-x: hidden;
        flex-direction: column;
        justify-content: stretch;
        align-items: flex-end;
    }

    .footer {
        position: absolute;
        bottom: 0;
        width: 100%;
        height: 100px;
        border-top: grey solid 1px;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-evenly;
    }

    button {
        border-radius: 10px;
        background-color: white;
        border: grey solid 1px;
        height: 45px;
        width: 80px;
    }
    .reset-button {
        background-color: lightcoral;
    }

    .kanji-list {
        height: 100%;
        position: fixed;
        top: 0;
        display: flex;
        flex-direction: row;
        align-items: center;
    }

    .list-opener {
        width: 15px;
        height: 100%;
        background-color: lightgoldenrodyellow;
        border-right: grey solid 1px;
        text-align: center;
        font-size: 15px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        user-select: none;
    }

    .list-element {
        width: 500px;
        overflow: hidden;
        background-color: white;
        border-right: grey 1px solid;
        height: 100%;
        overflow-y: scroll;
        display: flex;
        flex-direction: column;
        padding: 0;
    }

    .kanji-level-list {
        list-style: none;
        font-size: 20px;
        border-bottom: grey 1px solid;
        padding-bottom: 30px;
    }

    .listClosed {
        width: 0;
        padding: 0;
    }

    .kanji-box {
        font-size: 200px;
        height: 290px;
        display: flex;
        flex-direction: column;
        justify-content: stretch;
        align-items: center;
    }

    .kanji-trainer {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        text-align: center;
        width: calc(100% - 15px);
    }

    .trainer-input {
        display: flex;
        flex-direction: row;
    }

    .input-box {
        /*border-top: grey 1px solid;*/
        height: 100px;
        width: 50%;
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: center;
    }

    .left-border {
        border-left: grey solid 1px;
    }
    .right-border {
        border-right: grey solid 1px;
    }

    .input-button {
        width: 160px;
    }

    .selected {
        background-color: lightblue;
    }

    .mode-picker {
        position: fixed;
        top: 10px;
        right: 20px;
        display: flex;
        flex-direction: column;
        height: 200px;
        text-align: center;
        justify-content: space-between;
    }

</style>
<main>
    <div class="mode-picker">
        <h3>Pick mode</h3>
        <button on:click={() => mode = 0} on:click={() => combo = 0}>Kanji</button>
        <button on:click={() => mode = 1} on:click={() => combo = 0}>Hiragana</button>
        <button on:click={() => mode = 2} on:click={() => combo = 0}>Katakana</button>
    </div>
    <div on:click={() => listClosed = true} class="main-box">
            <div class="kanji-trainer">
                {#if mode === 0}
                <h1>Kanji trainer | Combo: {combo}</h1>
                {/if}
                {#if mode === 1}
                <h1>Hiragana trainer | Combo: {combo}</h1>
                {/if}
                {#if mode === 2}
                <h1>Katakana trainer | Combo: {combo}</h1>
                {/if}

                {#if mode === 0}
                    {#if kanjiTrainObject !== undefined}
                        {#if kanjiTrainObject["kanji"] !== undefined}
                            <div class="kanji-box">{kanjiTrainObject["kanji"]["New (Shinjitai)"]}
                                <button on:click={GuessKanji}>Pass</button>
                            </div>
                            <div class="trainer-input">
                                <div class="input-box english-input right-border ">
                                    {#each kanjiTrainObject["englishOptions"] as entry}
                                        {#if entry.selected}
                                            <button value={entry.value} on:click={SelectMeaning} class="input-button selected">{entry.value}</button>
                                        {/if}
                                        {#if !entry.selected}
                                            <button value={entry.value} on:click={SelectMeaning} class="input-button">{entry.value}</button>
                                        {/if}
                                    {/each}
                                </div>
                                <div class="input-box japanese-input left-border">
                                    {#each kanjiTrainObject["japaneseOptions"] as entry}
                                        {#if entry.selected}
                                            <button value={entry.value} on:click={SelectPronounciation} class="input-button selected">{entry.value}</button>
                                        {/if}
                                        {#if !entry.selected}
                                            <button value={entry.value} on:click={SelectPronounciation} class="input-button">{entry.value}</button>
                                        {/if}
                                    {/each}
                                </div>
                            </div>
                        {/if}
                    {/if}
                {/if}
                {#if mode === 1}
                    {#if hiraganaTrainObject !== undefined}
                        {#if hiraganaTrainObject["Hiragana"] !== undefined}
                            <div class="kanji-box">{hiraganaTrainObject["Hiragana"]["Hiragana"]}
                            </div>
                            <div class="trainer-input">
                                <div class="input-box">
                                    {#each hiraganaTrainObject["Readings"] as entry}
                                        {#if entry.selected}
                                            <button value={entry.value} on:click={SelectHiragana} class="input-button selected">{entry.value}</button>
                                        {/if}
                                        {#if !entry.selected}
                                            <button value={entry.value} on:click={SelectHiragana} class="input-button">{entry.value}</button>
                                        {/if}
                                    {/each}
                                </div>
                                <button on:click={GuessHiragana}>Pass</button>
                                <div class="input-box">
                                    <label>
                                        Text input
                                        <input bind:value={selectedHiragana} on:keydown={TextGuessHira}>
                                    </label>
                                    <label>
                                        Manual enter
                                        <input type="checkbox" bind:checked={manualEnter}>
                                    </label>
                                </div>
                            </div>
                        {/if}
                    {/if}
                {/if}
                {#if mode === 2}
                    {#if katakanaTrainObject !== undefined}
                        {#if katakanaTrainObject["Katakana"] !== undefined}
                            <div class="kanji-box">{katakanaTrainObject["Katakana"]["Katakana"]}
                            </div>
                            <div class="trainer-input">
                                <div class="input-box  ">
                                    {#each katakanaTrainObject["Readings"] as entry}
                                        {#if entry.selected}
                                            <button value={entry.value} on:click={SelectKatakana} class="input-button selected">{entry.value}</button>
                                        {/if}
                                        {#if !entry.selected}
                                            <button value={entry.value} on:click={SelectKatakana} class="input-button">{entry.value}</button>
                                        {/if}
                                    {/each}
                                </div>
                                <button on:click={GuessKatakana}>Pass</button>
                                <div class="input-box">
                                    <label>
                                        Text input
                                        <input on:keydown={TextGuessKata}>
                                    </label>
                                    <label>
                                        Manual enter
                                        <input type="checkbox" bind:checked={manualEnter}>
                                    </label>
                                </div>
                            </div>
                        {/if}
                    {/if}
                {/if}
            </div>
    </div>

    <div on:click={() => listClosed = true} class="footer">
        <button on:click={ResetDatabase} class="reset-button">Reset progress</button>
        <button on:click={() => OnAddKanji(1)}>Add Kanji lvl 1</button>
        <button on:click={() => OnAddKanji(2)}>Add Kanji lvl 2</button>
        <button on:click={() => OnAddKanji(3)}>Add Kanji lvl 3</button>
        <button on:click={() => OnAddKanji(4)}>Add Kanji lvl 4</button>
        <button on:click={() => OnAddKanji(5)}>Add Kanji lvl 5</button>
        <button on:click={() => OnAddKanji(6)}>Add Kanji lvl 6</button>
        <button on:click={() => OnAddKanji("S")}>Add Kanji lvl Secondary</button>
    </div>

    <div class="kanji-list">
        <div on:click={OpenList} class="list-opener">
            {#if listClosed}
                &gt;
            {/if}
            {#if !listClosed}
                &lt;
            {/if}
        </div>
        <ul class="list-element" class:listClosed>
            {#each Object.entries(kanjiLists) as [grade, list]}
                <ul class="kanji-level-list">
                    <h3>Grade {grade} Kanji:</h3>
                    {#each list as kanjiObject}
                        <li>{TextFromKanjiObject(kanjiObject)}</li>
                    {/each}
                </ul>
            {/each}
        </ul>
    </div>
</main>
