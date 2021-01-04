CREATE TABLE IF NOT EXISTS public.music (
    title text NOT NULL,
    pos integer DEFAULT 0 NOT NULL,
    link text NOT NULL,
    id_music integer NOT NULL,
    author text NOT NULL,
    voted_users text[],
    mark integer DEFAULT 0,
    message_id text
);