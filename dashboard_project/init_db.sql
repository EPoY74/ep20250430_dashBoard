create role :"u" with login password ':u';
create database :"u" owner :"u";
GRANT CONNECT ON DATABASE :"u" TO :"u";
GRANT USAGE ON SCHEMA public TO :"u";
GRANT CREATE ON SCHEMA public TO :"u";
-- \set dbname :u
-- \set dbuser :u
-- \set dbpass :u
-- \connect -reuse-previous=on dbname=:dbname user=:dbuser password=:dbpass
-- \connect -reuse-previous=on "dbname=:u user=:u password=:u"
\c :u :u
-- \connect -reuse-previous=on "dbname=':u' user=':u' password=':u' host=localhost"
-- \c dbname=:u user=:u password=:u port=5432 host=localhost
-- \connect -reuse-previous=on dbname=':u' user=':u' password=':u'
\i create_healt_table.sql