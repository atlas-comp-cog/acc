from clld.web.maps import Map, ParameterMap


def options(req):
    return dict(tile_layer=dict(
        url_pattern=req.static_url('acc:static/map_tiles/') + '{z}/{x}/{y}.png',
        options={
            'icons': 'custom',
            'minZoom': 0,
            'maxZoom': 1,
            'attribution': '',
            'worldCopyJump': False,
            'tms': True,
            #'maxBounds': 'L.latLngBounds(L.latLng(-90, -180), L.latLng(90, 180))',
            #'maxBoundsViscosity': 1.0,
        }))


class ACCMapMixin:
    def get_options(self):
        return options(self.req)

    def get_legends(self):
        for l in ParameterMap.get_legends(self):
            if l.name != 'iconsize':
                yield l


class TreeOfLife(ACCMapMixin, Map):
    pass


class CapacityMap(ACCMapMixin, ParameterMap):
    pass


def includeme(config):
    config.register_map('parameter', CapacityMap)
    config.register_map('languages', TreeOfLife)
