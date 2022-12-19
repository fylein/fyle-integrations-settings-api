--
-- PostgreSQL database dump
--

-- Dumped from database version 14.3
-- Dumped by pg_dump version 14.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_tokens; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_tokens (
    id integer NOT NULL,
    refresh_token text NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.auth_tokens OWNER TO postgres;

--
-- Name: bamboohr; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bamboohr (
    id integer NOT NULL,
    folder_id character varying(255),
    package_id character varying(255),
    api_token character varying(255),
    sub_domain character varying(255),
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    org_id integer NOT NULL
);


ALTER TABLE public.bamboohr OWNER TO postgres;

--
-- Name: bamboohr_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.bamboohr_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.bamboohr_id_seq OWNER TO postgres;

--
-- Name: bamboohr_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.bamboohr_id_seq OWNED BY public.bamboohr.id;


--
-- Name: configurations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.configurations (
    id integer NOT NULL,
    recipe_id character varying(255),
    recipe_data text,
    recipe_status boolean,
    additional_email_options jsonb,
    org_id integer NOT NULL,
    emails_selected jsonb
);


ALTER TABLE public.configurations OWNER TO postgres;

--
-- Name: configurations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.configurations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.configurations_id_seq OWNER TO postgres;

--
-- Name: configurations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.configurations_id_seq OWNED BY public.configurations.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO postgres;

--
-- Name: fyle_credentials; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.fyle_credentials (
    id integer NOT NULL,
    refresh_token text NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    org_id integer NOT NULL
);


ALTER TABLE public.fyle_credentials OWNER TO postgres;

--
-- Name: fyle_credentials_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.fyle_credentials_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fyle_credentials_id_seq OWNER TO postgres;

--
-- Name: fyle_credentials_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.fyle_credentials_id_seq OWNED BY public.fyle_credentials.id;


--
-- Name: fyle_rest_auth_authtokens_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.fyle_rest_auth_authtokens_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.fyle_rest_auth_authtokens_id_seq OWNER TO postgres;

--
-- Name: fyle_rest_auth_authtokens_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.fyle_rest_auth_authtokens_id_seq OWNED BY public.auth_tokens.id;


--
-- Name: orgs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orgs (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    fyle_org_id character varying(255) NOT NULL,
    managed_user_id character varying(255),
    cluster_domain character varying(255) NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    is_fyle_connected boolean,
    is_sendgrid_connected boolean
);


ALTER TABLE public.orgs OWNER TO postgres;

--
-- Name: orgs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orgs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orgs_id_seq OWNER TO postgres;

--
-- Name: orgs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orgs_id_seq OWNED BY public.orgs.id;


--
-- Name: orgs_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orgs_user (
    id integer NOT NULL,
    org_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.orgs_user OWNER TO postgres;

--
-- Name: orgs_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.orgs_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.orgs_user_id_seq OWNER TO postgres;

--
-- Name: orgs_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.orgs_user_id_seq OWNED BY public.orgs_user.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    id integer NOT NULL,
    email character varying(255) NOT NULL,
    user_id character varying(255) NOT NULL,
    full_name character varying(255) NOT NULL,
    active boolean NOT NULL,
    staff boolean NOT NULL,
    admin boolean NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_tokens id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_tokens ALTER COLUMN id SET DEFAULT nextval('public.fyle_rest_auth_authtokens_id_seq'::regclass);


--
-- Name: bamboohr id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bamboohr ALTER COLUMN id SET DEFAULT nextval('public.bamboohr_id_seq'::regclass);


--
-- Name: configurations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.configurations ALTER COLUMN id SET DEFAULT nextval('public.configurations_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: fyle_credentials id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fyle_credentials ALTER COLUMN id SET DEFAULT nextval('public.fyle_credentials_id_seq'::regclass);


--
-- Name: orgs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orgs ALTER COLUMN id SET DEFAULT nextval('public.orgs_id_seq'::regclass);


--
-- Name: orgs_user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orgs_user ALTER COLUMN id SET DEFAULT nextval('public.orgs_user_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add permission	1	add_permission
2	Can change permission	1	change_permission
3	Can delete permission	1	delete_permission
4	Can view permission	1	view_permission
5	Can add group	2	add_group
6	Can change group	2	change_group
7	Can delete group	2	delete_group
8	Can view group	2	view_group
9	Can add content type	3	add_contenttype
10	Can change content type	3	change_contenttype
11	Can delete content type	3	delete_contenttype
12	Can view content type	3	view_contenttype
13	Can add session	4	add_session
14	Can change session	4	change_session
15	Can delete session	4	delete_session
16	Can view session	4	view_session
17	Can add auth token	5	add_authtoken
18	Can change auth token	5	change_authtoken
19	Can delete auth token	5	delete_authtoken
20	Can view auth token	5	view_authtoken
21	Can add user	6	add_user
22	Can change user	6	change_user
23	Can delete user	6	delete_user
24	Can view user	6	view_user
25	Can add bamboo hr	7	add_bamboohr
26	Can change bamboo hr	7	change_bamboohr
27	Can delete bamboo hr	7	delete_bamboohr
28	Can view bamboo hr	7	view_bamboohr
29	Can add configuration	8	add_configuration
30	Can change configuration	8	change_configuration
31	Can delete configuration	8	delete_configuration
32	Can view configuration	8	view_configuration
33	Can add org	9	add_org
34	Can change org	9	change_org
35	Can delete org	9	delete_org
36	Can view org	9	view_org
37	Can add fyle credential	10	add_fylecredential
38	Can change fyle credential	10	change_fylecredential
39	Can delete fyle credential	10	delete_fylecredential
40	Can view fyle credential	10	view_fylecredential
\.


--
-- Data for Name: auth_tokens; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.auth_tokens (id, refresh_token, user_id) FROM stdin;
\.


--
-- Data for Name: bamboohr; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bamboohr (id, folder_id, package_id, api_token, sub_domain, created_at, updated_at, org_id) FROM stdin;
\.


--
-- Data for Name: configurations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.configurations (id, recipe_id, recipe_data, recipe_status, additional_email_options, org_id, emails_selected) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	auth	permission
2	auth	group
3	contenttypes	contenttype
4	sessions	session
5	fyle_rest_auth	authtoken
6	users	user
7	bamboohr	bamboohr
8	bamboohr	configuration
9	orgs	org
10	orgs	fylecredential
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2022-12-19 16:37:16.895848+05:30
2	contenttypes	0002_remove_content_type_name	2022-12-19 16:37:16.903269+05:30
3	auth	0001_initial	2022-12-19 16:37:16.922727+05:30
4	auth	0002_alter_permission_name_max_length	2022-12-19 16:37:16.971383+05:30
5	auth	0003_alter_user_email_max_length	2022-12-19 16:37:16.975006+05:30
6	auth	0004_alter_user_username_opts	2022-12-19 16:37:16.978515+05:30
7	auth	0005_alter_user_last_login_null	2022-12-19 16:37:16.982361+05:30
8	auth	0006_require_contenttypes_0002	2022-12-19 16:37:16.983434+05:30
9	auth	0007_alter_validators_add_error_messages	2022-12-19 16:37:16.986741+05:30
10	auth	0008_alter_user_username_max_length	2022-12-19 16:37:16.991014+05:30
11	auth	0009_alter_user_last_name_max_length	2022-12-19 16:37:16.994258+05:30
12	auth	0010_alter_group_name_max_length	2022-12-19 16:37:17.000773+05:30
13	auth	0011_update_proxy_permissions	2022-12-19 16:37:17.00471+05:30
14	auth	0012_alter_user_first_name_max_length	2022-12-19 16:37:17.00829+05:30
15	users	0001_initial	2022-12-19 16:37:17.015675+05:30
16	orgs	0001_initial	2022-12-19 16:37:17.04656+05:30
17	bamboohr	0001_initial	2022-12-19 16:37:17.074421+05:30
18	bamboohr	0002_configuration	2022-12-19 16:37:17.099385+05:30
19	bamboohr	0003_auto_20221212_1052	2022-12-19 16:37:17.113784+05:30
20	fyle_rest_auth	0001_initial	2022-12-19 16:37:17.124536+05:30
21	fyle_rest_auth	0002_auto_20200101_1205	2022-12-19 16:37:17.158466+05:30
22	fyle_rest_auth	0003_auto_20200107_0921	2022-12-19 16:37:17.170733+05:30
23	fyle_rest_auth	0004_auto_20200107_1345	2022-12-19 16:37:17.182769+05:30
24	fyle_rest_auth	0005_remove_authtoken_access_token	2022-12-19 16:37:17.186851+05:30
25	fyle_rest_auth	0006_auto_20201221_0849	2022-12-19 16:37:17.191688+05:30
26	orgs	0002_auto_20221219_1044	2022-12-19 16:37:17.205446+05:30
27	sessions	0001_initial	2022-12-19 16:37:17.213626+05:30
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: fyle_credentials; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.fyle_credentials (id, refresh_token, created_at, updated_at, org_id) FROM stdin;
\.


--
-- Data for Name: orgs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orgs (id, name, fyle_org_id, managed_user_id, cluster_domain, created_at, updated_at, is_fyle_connected, is_sendgrid_connected) FROM stdin;
\.


--
-- Data for Name: orgs_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orgs_user (id, org_id, user_id) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (password, last_login, id, email, user_id, full_name, active, staff, admin) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 40, true);


--
-- Name: bamboohr_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.bamboohr_id_seq', 1, false);


--
-- Name: configurations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.configurations_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 10, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 27, true);


--
-- Name: fyle_credentials_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.fyle_credentials_id_seq', 1, false);


--
-- Name: fyle_rest_auth_authtokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.fyle_rest_auth_authtokens_id_seq', 1, false);


--
-- Name: orgs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orgs_id_seq', 1, false);


--
-- Name: orgs_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orgs_user_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 1, false);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: bamboohr bamboohr_org_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bamboohr
    ADD CONSTRAINT bamboohr_org_id_key UNIQUE (org_id);


--
-- Name: bamboohr bamboohr_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bamboohr
    ADD CONSTRAINT bamboohr_pkey PRIMARY KEY (id);


--
-- Name: configurations configurations_org_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.configurations
    ADD CONSTRAINT configurations_org_id_key UNIQUE (org_id);


--
-- Name: configurations configurations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.configurations
    ADD CONSTRAINT configurations_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: fyle_credentials fyle_credentials_org_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fyle_credentials
    ADD CONSTRAINT fyle_credentials_org_id_key UNIQUE (org_id);


--
-- Name: fyle_credentials fyle_credentials_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fyle_credentials
    ADD CONSTRAINT fyle_credentials_pkey PRIMARY KEY (id);


--
-- Name: auth_tokens fyle_rest_auth_authtokens_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_tokens
    ADD CONSTRAINT fyle_rest_auth_authtokens_pkey PRIMARY KEY (id);


--
-- Name: auth_tokens fyle_rest_auth_authtokens_user_id_3b4bd82e_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_tokens
    ADD CONSTRAINT fyle_rest_auth_authtokens_user_id_3b4bd82e_uniq UNIQUE (user_id);


--
-- Name: orgs orgs_fyle_org_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orgs
    ADD CONSTRAINT orgs_fyle_org_id_key UNIQUE (fyle_org_id);


--
-- Name: orgs orgs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orgs
    ADD CONSTRAINT orgs_pkey PRIMARY KEY (id);


--
-- Name: orgs_user orgs_user_org_id_user_id_091e68bb_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orgs_user
    ADD CONSTRAINT orgs_user_org_id_user_id_091e68bb_uniq UNIQUE (org_id, user_id);


--
-- Name: orgs_user orgs_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orgs_user
    ADD CONSTRAINT orgs_user_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_user_id_key UNIQUE (user_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: orgs_fyle_org_id_e8ddcc98_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX orgs_fyle_org_id_e8ddcc98_like ON public.orgs USING btree (fyle_org_id varchar_pattern_ops);


--
-- Name: orgs_user_org_id_b1e1cc06; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX orgs_user_org_id_b1e1cc06 ON public.orgs_user USING btree (org_id);


--
-- Name: orgs_user_user_id_78de0fc6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX orgs_user_user_id_78de0fc6 ON public.orgs_user USING btree (user_id);


--
-- Name: users_user_id_26693996_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX users_user_id_26693996_like ON public.users USING btree (user_id varchar_pattern_ops);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: bamboohr bamboohr_org_id_63ab7693_fk_orgs_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bamboohr
    ADD CONSTRAINT bamboohr_org_id_63ab7693_fk_orgs_id FOREIGN KEY (org_id) REFERENCES public.orgs(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: configurations configurations_org_id_ddcda5f1_fk_orgs_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.configurations
    ADD CONSTRAINT configurations_org_id_ddcda5f1_fk_orgs_id FOREIGN KEY (org_id) REFERENCES public.orgs(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fyle_credentials fyle_credentials_org_id_1c21aedd_fk_orgs_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.fyle_credentials
    ADD CONSTRAINT fyle_credentials_org_id_1c21aedd_fk_orgs_id FOREIGN KEY (org_id) REFERENCES public.orgs(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_tokens fyle_rest_auth_authtokens_user_id_3b4bd82e_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.auth_tokens
    ADD CONSTRAINT fyle_rest_auth_authtokens_user_id_3b4bd82e_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orgs_user orgs_user_org_id_b1e1cc06_fk_orgs_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orgs_user
    ADD CONSTRAINT orgs_user_org_id_b1e1cc06_fk_orgs_id FOREIGN KEY (org_id) REFERENCES public.orgs(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: orgs_user orgs_user_user_id_78de0fc6_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.orgs_user
    ADD CONSTRAINT orgs_user_user_id_78de0fc6_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

