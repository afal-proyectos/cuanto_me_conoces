-- ============================================
-- TABLA: quizzes
-- ============================================
create table quizzes (
    id uuid primary key default gen_random_uuid(),
    creator_name text not null,
    title text not null,
    status text default 'open',       -- 'open' | 'closed'
    created_at timestamptz default now()
);


create policy "cualquiera puede crear un quiz"
    on quizzes for insert
    with check (true);

create policy "cualquiera puede leer un quiz"
    on quizzes for select
    using (true);


-- ============================================
-- TABLA: questions
-- ============================================
create table questions (
    id uuid primary key default gen_random_uuid(),
    quiz_id uuid references quizzes(id) on delete cascade,
    order_index int not null,
    question_text text not null,
    options jsonb not null,           -- ["Opción A", "Opción B", "Opción C"]
    correct_answer text not null,     -- para v1: solo opción múltiple, un solo string
    points int default 10
);

alter table questions enable row level security;

create policy "cualquiera puede crear preguntas"
    on questions for insert
    with check (true);

create policy "cualquiera puede leer preguntas"
    on questions for select
    using (true);


-- ============================================
-- TABLA: players
-- ============================================
create table players (
    id uuid primary key default gen_random_uuid(),
    quiz_id uuid references quizzes(id) on delete cascade,
    player_name text not null,
    joined_at timestamptz default now()
);

alter table players enable row level security;

create policy "cualquiera puede registrarse como jugador"
    on players for insert
    with check (true);

create policy "cualquiera puede leer jugadores"
    on players for select
    using (true);


-- ============================================
-- TABLA: results
-- ============================================
create table results (
    id uuid primary key default gen_random_uuid(),
    player_id uuid references players(id) on delete cascade,
    quiz_id uuid references quizzes(id) on delete cascade,
    answers jsonb not null,           -- [{"question_id": "...", "answer": "..."}]
    score int not null,
    submitted_at timestamptz default now()
);

alter table results enable row level security;

create policy "cualquiera puede enviar resultados"
    on results for insert
    with check (true);

create policy "cualquiera puede leer resultados (para el ranking)"
    on results for select
    using (true);
