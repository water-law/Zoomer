```
CREATE DATABASE place TEMPLATE=postgis_24_sample;
CREATE TYPE objl_type AS ENUM ('Administrator area(Named)', 'Airport/airfield', 'Bridge', 'Building, single', 'Built-up, area', 'Canal',
'Cargo transshipment area', 'Causeway', 'Fairway', 'Fence line', 'Fishery zone', 'Freeport area', 'Harbor area(administrative)', 'Ice area',
'Lake', 'Land area', 'Land elevation', 'Land region', 'Landmark', 'Pontoon', 'Production/storage area', 'Railway', 'Recommended route center line',
'Recommended track', 'Restricted area', 'River', 'Road', 'Runway', 'Sea area/named water area', 'Seabed area', 'Shore line construction',
'Tunnel', 'Underwater/awash rock');
CREATE TABLE objnam (
    fid int4 PRIMARY KEY,
    objl objl_type,
    scamax int4,
    scamin int4,
    zh_chs text,
    en_us text
);
SELECT AddGeometryColumn ('objnam', 'geom', 4326, 'POINT', 2);
INSERT INTO objnam (fid, geom, objl) VALUES (1,ST_GeomFromText('POINT(-0.1257 51.508)',4326), 'Administrator area(Named)');
INSERT INTO objnam (fid, geom, objl) VALUES (2,ST_GeomFromText('POINT(-81.233 42.983)',4326),'Landmark');
INSERT INTO objnam (fid, geom, objl) VALUES (3,ST_GeomFromText('POINT(27.91162491 -33.01529)',4326),'Sea area/named water area');
```

[参考链接](http://live.osgeo.org/zh/quickstart/postgis_quickstart.html)