manual_genre_map = {
    # UK Indie/Rock Bands
    'Pentire': 'indie',
    'M60': 'indie',  # Changed from bassline - they're indie/bassline
    'Wunderhorse': 'indie',
    'Sam Fender': 'indie',
    'The Lathums': 'indie',
    'The Clause': 'indie',
    'Inhaler': 'indie',
    'The Guest List': 'indie',
    'The Lilacs': 'indie',
    'overpass': 'indie',
    'The Reytons': 'indie',
    'Basht.': 'indie',
    'Alex Spencer': 'indie',
    'Danny Mellin': 'indie',
    'Keyside': 'indie',
    'CRUZ': 'indie',
    'Arkayla': 'indie',
    'Tom A. Smith': 'indie',
    'Arthur Hill': 'indie',
    'Djo': 'indie',
    'Louis Dunford': 'indie',
    'The Royston Club': 'indie',
    
    # Welsh Language Artists
    'Bwncath': 'welsh_indie',
    'Gwilym': 'welsh_indie',
    'Candelas': 'welsh_indie',
    'Breichiau Hir': 'welsh_folk',
    'Y Bandana': 'welsh_folk',
    'Y Cyrff': 'welsh_folk',
    'Fleur De Lys': 'welsh_folk',
    'Al Lewis Band': 'welsh_indie',
    'Y Cledrau': 'welsh_indie',
    'Mellt': 'welsh_indie',
    'Yws Gwynedd': 'welsh_indie',
    'Bryn Fôn': 'welsh_folk',
    'Sŵnami': 'welsh_indie',
    
    # Other Artists
    'Hozier': 'indie',
    'Ren': 'alternative',
    'Evan Honer': 'indie',
    'Julia DiGrazia': 'indie',
    'Eden Nash': 'alternative',
    'Kingfishr': 'indie',
    'Twenty One Pilots': 'alternative',
    'Benson Boone': 'pop',
    'Malcolm Todd': 'indie',
    'INOHA': 'indie',
    'Ben Kidson': 'indie',
    'Elton John': 'classic_rock',
    'FINNEAS': 'pop',
    'Paolo Nutini': 'indie',
    'Gorillaz': 'alternative',
    'Dominic Fike': 'indie',
    'Cameron Winter': 'indie',
    'Somebody\'s Child': 'indie',
    'Neutral Milk Hotel': 'indie',
}

genre_groups = {
    # Indie/Rock family (your main music)
    'indie': 'indie_rock',
    'post-punk': 'indie_rock',
    'britpop': 'indie_rock',
    'alternative rock': 'indie_rock',
    'midwest emo': 'indie_rock',
    'alternative': 'indie_rock',
    'indie folk': 'indie_rock',
    'art rock': 'indie_rock',
    'anti-folk': 'indie_rock',
    'post-rock': 'indie_rock',
    'neo-psychedelic': 'indie_rock',
    'proto-punk': 'indie_rock',
    
    # Electronic/Dance
    'drum and bass': 'electronic',
    'tech house': 'electronic',
    'grime': 'electronic',
    'uk garage': 'electronic',
    
    # Welsh Music
    'welsh_indie': 'welsh',
    'welsh_folk': 'welsh',
    'traditional folk': 'welsh',
    'classical': 'welsh',  # All classical music in the dataset is currently Welsh (can be changed if my music taste goes there eventually)
    
    # Pop/Soul
    'pop soul': 'pop',
    'bedroom pop': 'pop',
    'pop': 'pop',
    
    # Retro/Other
    'doo-wop': 'retro',
    'classic rock': 'retro',
    'folk': 'folk',
    'blues': 'blues',
    'soundtrack': 'other',
}