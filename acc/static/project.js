CLLD.MapIcons.custom = function (feature, size, url) {
    size = 30;
    return L.icon({
        iconUrl: url == undefined ? feature.properties.icon : url,
        iconSize: [size, size],
        iconAnchor: [Math.floor(size / 2), Math.floor(size / 2)],
        popupAnchor: [0, 0],
        className: feature.properties['class'] == undefined ? 'clld-map-icon' : feature.properties['class']
    });
};

CLLD.mapResizeIcons = function(eid, size) {};
