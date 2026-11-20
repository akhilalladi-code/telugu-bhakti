const toggle=document.querySelector('.menu-toggle');
const nav=document.querySelector('.nav');
if(toggle&&nav){toggle.addEventListener('click',()=>{const open=nav.classList.toggle('open');toggle.setAttribute('aria-expanded',String(open));});}
document.querySelectorAll('[data-year]').forEach(el=>el.textContent=new Date().getFullYear());

const copyLyricsButton=document.querySelector('[data-copy-lyrics]');
if(copyLyricsButton){
  copyLyricsButton.addEventListener('click',async()=>{
    const node=document.querySelector('#song-lyrics');
    const lyrics=node?.textContent||'';
    try{
      if(!navigator.clipboard?.writeText) throw new Error('Clipboard API unavailable');
      await navigator.clipboard.writeText(lyrics);
      copyLyricsButton.textContent='కాపీ అయింది ✓';
      copyLyricsButton.setAttribute('aria-live','polite');
      window.setTimeout(()=>copyLyricsButton.textContent='సాహిత్యం కాపీ చేయండి',1800);
    }catch(error){
      if(node){
        const range=document.createRange();
        range.selectNodeContents(node);
        const selection=window.getSelection();
        selection?.removeAllRanges();
        selection?.addRange(range);
        copyLyricsButton.textContent='సాహిత్యం సెలెక్ట్ అయింది — Copy చేయండి';
      }
    }
  });
}

const searchInput=document.querySelector('#song-search-input');
const searchResults=document.querySelector('#song-search-results');
const searchStatus=document.querySelector('#song-search-status');
const searchClear=document.querySelector('#song-search-clear');
if(searchInput&&searchResults&&searchStatus){
  const normalize=value=>String(value||'').toLocaleLowerCase().normalize('NFC').trim();
  let songs=[];
  fetch('data/songs.json')
    .then(response=>{if(!response.ok)throw new Error('Song index unavailable');return response.json();})
    .then(data=>{songs=Array.isArray(data)?data:[];searchStatus.textContent=songs.length? `${songs.length} పాట అందుబాటులో ఉంది. వెతకడం ప్రారంభించండి.`:'ప్రస్తుతం పాటలు అందుబాటులో లేవు.';})
    .catch(()=>{searchStatus.textContent='పాటల జాబితా లోడ్ కాలేదు. దయచేసి మళ్లీ ప్రయత్నించండి.';});
  const render=()=>{
    const query=normalize(searchInput.value);
    searchResults.replaceChildren();
    if(!query){searchStatus.textContent=songs.length?`${songs.length} పాట అందుబాటులో ఉంది. వెతకడం ప్రారంభించండి.`:'పాటల జాబితా లోడ్ అవుతోంది.';return;}
    const matches=songs.filter(song=>normalize([song.titleTe,song.titleEn,song.deity,song.category,song.description,...(song.keywords||[])].join(' ')).includes(query));
    searchStatus.textContent=matches.length?`${matches.length} ఫలితాలు కనుగొనబడ్డాయి.`:'ఫలితాలు కనబడలేదు. వేరే పదంతో వెతకండి.';
    matches.forEach(song=>{
      const link=document.createElement('a');
      link.className='search-result';
      link.href=song.href;
      const title=document.createElement('strong');
      title.textContent=song.titleTe;
      const meta=document.createElement('small');
      meta.textContent=[song.titleEn,song.deity,song.category].filter(Boolean).join(' · ');
      link.append(title,meta);
      searchResults.append(link);
    });
  };
  searchInput.addEventListener('input',render);
  searchClear?.addEventListener('click',()=>{searchInput.value='';render();searchInput.focus();});
}
