//test
document.addEventListener("DOMContentLoaded", ()=> {
    lightbox()
    const image = document.getElementById('watchlist');
    const id = image.dataset.id;
    image.src = watchlist_check(image.dataset.watchlist);

    image.onclick = ()=> {
        fetch(`/api/watchlistToggle/${id}`).then(response => response.json()).then(data => {
            console.log(data);
            update_icon(data);

        })
    }
})

function lightbox(){
    const imageInstance = basicLightbox.create(document.querySelector('#image'))
    document.querySelector('img.image').onclick = imageInstance.show
}

function watchlist_check(inWatchlist){

    if (inWatchlist == 'True'){
        filename = '/auctions/static/auctions/on.png';
    }
    else{
        filename = '/auctions/static/auctions/off.png';
    }
    return filename
}

function update_icon(data){
    var newstate = data["current_value"];
    var filename = `/auctions/static/auctions/${newstate}.png`;
    document.getElementById('watchlist').src = filename;
}