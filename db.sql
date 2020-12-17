CREATE TABLE IF NOT EXISTS public.music
(
    title text COLLATE pg_catalog."default" NOT NULL,
    pos integer NOT NULL DEFAULT 0,
    link text COLLATE pg_catalog."default" NOT NULL,
    id_music integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    author text COLLATE pg_catalog."default" NOT NULL,
    voted_users integer[],
    mark integer DEFAULT 0,
    CONSTRAINT music_pkey PRIMARY KEY (id_music)
)