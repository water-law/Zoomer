CREATE DATABASE demo TEMPLATE=postgis_24_sample;
CREATE TYPE objl_type AS ENUM ('111', '112', '113');
CREATE TYPE level_type AS ENUM ('1', '2', '3');
CREATE TABLE objnam (
    id serial PRIMARY KEY,
    fid int4,
    objl objl_type,
    scamax int4,
    scamin int4,
    level level_type,
    zh_chs text,
    en_us text
);
SELECT AddGeometryColumn ('objnam', 'geom', 4326, 'POINT', 2);
INSERT INTO objnam (fid, geom, objl) VALUES (1,ST_GeomFromText('POINT(-0.1257 51.508)',4326), '111');
INSERT INTO objnam (fid, geom, objl) VALUES (2,ST_GeomFromText('POINT(-81.233 42.983)',4326),'112');
INSERT INTO objnam (fid, geom, objl) VALUES (3,ST_GeomFromText('POINT(27.91162491 -33.01529)',4326),'113');

[参考链接](http://live.osgeo.org/zh/quickstart/postgis_quickstart.html)