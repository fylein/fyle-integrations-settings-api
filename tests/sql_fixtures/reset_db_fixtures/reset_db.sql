--
-- PostgreSQL database dump
--

-- Dumped from database version 14.6 (Homebrew)
-- Dumped by pg_dump version 14.6 (Homebrew)

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
-- Name: bamboohr_configurations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bamboohr_configurations (
    id integer NOT NULL,
    recipe_id character varying(255),
    recipe_data text,
    recipe_status boolean,
    additional_email_options jsonb,
    org_id integer NOT NULL,
    emails_selected jsonb
);


ALTER TABLE public.bamboohr_configurations OWNER TO postgres;

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

ALTER SEQUENCE public.configurations_id_seq OWNED BY public.bamboohr_configurations.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


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
-- Name: travelperk; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.travelperk (
    id integer NOT NULL,
    folder_id character varying(255),
    package_id character varying(255),
    is_fyle_connected boolean,
    is_s3_connected boolean,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    org_id integer NOT NULL,
    travelperk_connection_id integer
);


ALTER TABLE public.travelperk OWNER TO postgres;

--
-- Name: travelperk_configurations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.travelperk_configurations (
    id integer NOT NULL,
    recipe_id character varying(255),
    recipe_data text,
    is_recipe_enabled boolean,
    org_id integer NOT NULL
);


ALTER TABLE public.travelperk_configurations OWNER TO postgres;

--
-- Name: travelperk_configurations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.travelperk_configurations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.travelperk_configurations_id_seq OWNER TO postgres;

--
-- Name: travelperk_configurations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.travelperk_configurations_id_seq OWNED BY public.travelperk_configurations.id;


--
-- Name: travelperk_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.travelperk_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.travelperk_id_seq OWNER TO postgres;

--
-- Name: travelperk_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.travelperk_id_seq OWNED BY public.travelperk.id;


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
-- Name: bamboohr_configurations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bamboohr_configurations ALTER COLUMN id SET DEFAULT nextval('public.configurations_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


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
-- Name: travelperk id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.travelperk ALTER COLUMN id SET DEFAULT nextval('public.travelperk_id_seq'::regclass);


--
-- Name: travelperk_configurations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.travelperk_configurations ALTER COLUMN id SET DEFAULT nextval('public.travelperk_configurations_id_seq'::regclass);


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
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add auth token	6	add_authtoken
22	Can change auth token	6	change_authtoken
23	Can delete auth token	6	delete_authtoken
24	Can view auth token	6	view_authtoken
25	Can add user	7	add_user
26	Can change user	7	change_user
27	Can delete user	7	delete_user
28	Can view user	7	view_user
29	Can add bamboo hr	8	add_bamboohr
30	Can change bamboo hr	8	change_bamboohr
31	Can delete bamboo hr	8	delete_bamboohr
32	Can view bamboo hr	8	view_bamboohr
33	Can add configuration	9	add_configuration
34	Can change configuration	9	change_configuration
35	Can delete configuration	9	delete_configuration
36	Can view configuration	9	view_configuration
37	Can add org	10	add_org
38	Can change org	10	change_org
39	Can delete org	10	delete_org
40	Can view org	10	view_org
41	Can add fyle credential	11	add_fylecredential
42	Can change fyle credential	11	change_fylecredential
43	Can delete fyle credential	11	delete_fylecredential
44	Can view fyle credential	11	view_fylecredential
45	Can add bamboo hr configuration	9	add_bamboohrconfiguration
46	Can change bamboo hr configuration	9	change_bamboohrconfiguration
47	Can delete bamboo hr configuration	9	delete_bamboohrconfiguration
48	Can view bamboo hr configuration	9	view_bamboohrconfiguration
49	Can add travel perk	12	add_travelperk
50	Can change travel perk	12	change_travelperk
51	Can delete travel perk	12	delete_travelperk
52	Can view travel perk	12	view_travelperk
53	Can add travel perk configuration	13	add_travelperkconfiguration
54	Can change travel perk configuration	13	change_travelperkconfiguration
55	Can delete travel perk configuration	13	delete_travelperkconfiguration
56	Can view travel perk configuration	13	view_travelperkconfiguration
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
1	163	112	dummy	dummy	2022-12-06 14:42:38.724679+05:30	2022-12-06 14:43:33.008685+05:30	1
\.


--
-- Data for Name: bamboohr_configurations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bamboohr_configurations (id, recipe_id, recipe_data, recipe_status, additional_email_options, org_id, emails_selected) FROM stdin;
1	3429	{"number": 0, "provider": "bamboohr", "name": "updated_employee", "as": "6761c014", "title": null, "description": null, "keyword": "trigger", "dynamicPickListSelection": {}, "toggleCfg": {"flag": true}, "input": {"flag": "true"}, "extended_output_schema": [{"control_type": "text", "label": "NIN", "name": "customNIN1", "optional": true, "type": "string"}, {"control_type": "select", "label": "Secondary Language", "name": "customSecondaryLanguage1", "optional": true, "pick_list": [["French", "French"], ["German", "German"], ["Japanese", "Japanese"], ["Mandarin", "Mandarin"], ["Spanish", "Spanish"]], "toggle_field": {"control_type": "text", "label": "Secondary Language", "toggle_hint": "Enter custom value", "optional": true, "type": "string", "name": "customSecondaryLanguage1"}, "toggle_hint": "Select from list", "type": "string"}, {"control_type": "select", "label": "Shirt size", "name": "customShirtsize", "optional": true, "pick_list": [["1. Small", "1. Small"], ["2. Medium", "2. Medium"], ["3. Large", "3. Large"], ["4. XLarge", "4. XLarge"], ["5. XXLarge", "5. XXLarge"]], "toggle_field": {"control_type": "text", "label": "Shirt size", "toggle_hint": "Enter custom value", "optional": true, "type": "string", "name": "customShirtsize"}, "toggle_hint": "Select from list", "type": "string"}, {"control_type": "text", "label": "Tax File Number", "name": "customTaxFileNumber1", "optional": true, "type": "string"}], "block": [{"number": 1, "keyword": "try", "dynamicPickListSelection": {}, "toggleCfg": {}, "input": {}, "block": [{"number": 2, "keyword": "if", "dynamicPickListSelection": {}, "toggleCfg": {}, "input": {"type": "compound", "operand": "and", "conditions": [{"operand": "present", "lhs": "#{_('data.bamboohr.6761c014.supervisorEId')}", "rhs": "", "uuid": "condition-79dc736e-21b3-4f53-bcd3-eafef8a76362"}]}, "block": [{"number": 3, "provider": "bamboohr", "name": "get_employee_by_id", "as": "e5cf843b", "title": null, "description": null, "keyword": "action", "dynamicPickListSelection": {}, "toggleCfg": {}, "input": {"id": "#{_('data.bamboohr.6761c014.supervisorEId')}"}, "extended_output_schema": [{"control_type": "text", "label": "NIN", "name": "customNIN1", "optional": true, "type": "string"}, {"control_type": "select", "label": "Secondary Language", "name": "customSecondaryLanguage1", "optional": true, "pick_list": [["French", "French"], ["German", "German"], ["Japanese", "Japanese"], ["Mandarin", "Mandarin"], ["Spanish", "Spanish"]], "toggle_field": {"control_type": "text", "label": "Secondary Language", "toggle_hint": "Enter custom value", "optional": true, "type": "string", "name": "customSecondaryLanguage1"}, "toggle_hint": "Select from list", "type": "string"}, {"control_type": "select", "label": "Shirt size", "name": "customShirtsize", "optional": true, "pick_list": [["1. Small", "1. Small"], ["2. Medium", "2. Medium"], ["3. Large", "3. Large"], ["4. XLarge", "4. XLarge"], ["5. XXLarge", "5. XXLarge"]], "toggle_field": {"control_type": "text", "label": "Shirt size", "toggle_hint": "Enter custom value", "optional": true, "type": "string", "name": "customShirtsize"}, "toggle_hint": "Select from list", "type": "string"}, {"control_type": "text", "label": "Tax File Number", "name": "customTaxFileNumber1", "optional": true, "type": "string"}], "uuid": "587d07c1-2d4e-473a-853a-f768b441bd7c"}, {"number": 4, "provider": "fyle_staging_connector_892703_1670317976", "name": "search_employee", "as": "d02a328f", "title": null, "description": null, "keyword": "action", "dynamicPickListSelection": {}, "toggleCfg": {}, "input": {"email": "='eq.' + _('data.bamboohr.e5cf843b.workEmail')"}, "extended_output_schema": [{"label": "Employees", "name": "data", "of": "object", "optional": true, "properties": [{"control_type": "number", "label": "Count", "parse_output": "float_conversion", "optional": true, "type": "number", "name": "count"}, {"name": "data", "type": "array", "of": "object", "label": "Data", "optional": true, "properties": [{"control_type": "text", "label": "Branch account", "optional": true, "type": "string", "name": "branch_account"}, {"control_type": "text", "label": "Branch ifsc", "optional": true, "type": "string", "name": "branch_ifsc"}, {"control_type": "text", "label": "Business unit", "optional": true, "type": "string", "name": "business_unit"}, {"control_type": "text", "label": "Code", "optional": true, "type": "string", "name": "code"}, {"control_type": "text", "label": "Created at", "render_input": "date_time_conversion", "parse_output": "date_time_conversion", "optional": true, "type": "date_time", "name": "created_at"}, {"control_type": "text", "label": "Department", "optional": true, "type": "string", "name": "department"}, {"control_type": "text", "label": "Department ID", "optional": true, "type": "string", "name": "department_id"}, {"control_type": "text", "label": "Has accepted invite", "parse_output": {}, "render_input": {}, "toggle_hint": "Select from option list", "toggle_field": {"label": "Has accepted invite", "control_type": "text", "toggle_hint": "Use custom value", "type": "boolean", "name": "has_accepted_invite"}, "optional": true, "type": "number", "name": "has_accepted_invite"}, {"control_type": "text", "label": "ID", "optional": true, "type": "string", "name": "id"}, {"control_type": "text", "label": "Is enabled", "parse_output": {}, "render_input": {}, "toggle_hint": "Select from option list", "toggle_field": {"label": "Is enabled", "control_type": "text", "toggle_hint": "Use custom value", "type": "boolean", "name": "is_enabled"}, "optional": true, "type": "number", "name": "is_enabled"}, {"control_type": "text", "label": "Joined at", "render_input": "date_time_conversion", "parse_output": "date_time_conversion", "optional": true, "type": "date_time", "name": "joined_at"}, {"control_type": "text", "label": "Level", "optional": true, "type": "string", "name": "level"}, {"control_type": "text", "label": "Level ID", "optional": true, "type": "string", "name": "level_id"}, {"control_type": "text", "label": "Location", "optional": true, "type": "string", "name": "location"}, {"control_type": "text", "label": "Mobile", "optional": true, "type": "string", "name": "mobile"}, {"control_type": "text", "label": "Org ID", "optional": true, "type": "string", "name": "org_id"}, {"name": "roles", "type": "array", "of": "string", "label": "Roles", "optional": true}, {"control_type": "text", "label": "Special email", "optional": true, "type": "string", "name": "special_email"}, {"control_type": "text", "label": "Title", "optional": true, "type": "string", "name": "title"}, {"control_type": "text", "label": "Updated at", "render_input": "date_time_conversion", "parse_output": "date_time_conversion", "optional": true, "type": "date_time", "name": "updated_at"}, {"label": "User", "optional": true, "type": "object", "name": "user", "properties": [{"control_type": "text", "label": "Email", "optional": true, "type": "string", "name": "email"}, {"control_type": "text", "label": "Full name", "optional": true, "type": "string", "name": "full_name"}, {"control_type": "text", "label": "ID", "optional": true, "type": "string", "name": "id"}]}, {"control_type": "text", "label": "User ID", "optional": true, "type": "string", "name": "user_id"}]}, {"control_type": "number", "label": "Offset", "parse_output": "float_conversion", "optional": true, "type": "number", "name": "offset"}], "type": "array"}], "uuid": "55913e43-d3fd-451e-837a-445246be5c7f"}], "uuid": "499d0a9a-7aec-4b07-a106-30ca7589545a"}, {"number": 5, "provider": "fyle_staging_connector_892703_1670317976", "name": "create_employees_in_fyle", "as": "07f04431", "title": null, "description": null, "keyword": "action", "dynamicPickListSelection": {}, "toggleCfg": {}, "input": {"data": {"user_email": "#{_('data.bamboohr.6761c014.workEmail')}", "user_full_name": "#{_('data.bamboohr.6761c014.displayName')}", "title": "#{_('data.bamboohr.6761c014.jobTitle')}", "location": "#{_('data.bamboohr.6761c014.location')}", "is_enabled": "=_('data.bamboohr.6761c014.status').include?(\\"Active\\")", "approver_emails": "=_('data.fyle_staging_connector_892703_1670317976.d02a328f.data').present? ? [_('data.bamboohr.e5cf843b.workEmail')] : []"}}, "visible_config_fields": ["data", "data.is_enabled", "data.user_full_name", "data.user_email", "data.title", "data.location", "data.approver_emails"], "uuid": "36320f70-4509-46fe-80c3-fd89ac93a0dd", "skip": false}, {"number": 6, "as": "86be96e2", "keyword": "catch", "dynamicPickListSelection": {}, "toggleCfg": {}, "input": {"max_retry_count": "0", "retry_interval": "2"}, "block": [{"number": 7, "provider": "sendgrid", "name": "send_email", "as": "2c55fabe", "keyword": "action", "dynamicPickListSelection": {}, "toggleCfg": {}, "input": {"personalizations": {"to": {"email": "ni12lesh[amt1212@gmail.in"}}, "from": {"email": "notifications-staging@fylehq.com"}, "subject": "This Is A Test Email", "content": {"type": "text/plain", "value": "This is a Test Email From Workato"}}, "uuid": "93f8d230-00ae-456e-891c-653daa656dea"}], "uuid": "d6e76e57-08a2-4d26-a7c1-d74c92709d06"}], "uuid": "14f5a93e-8d8a-4659-8dba-ded9b816b173"}], "uuid": "9facdee0-dff2-4a3c-bf60-06265ca8a599"}	f	{"name": "Nilsh", "email": "dfoisdfoh@gmail.com"}	1	[]
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	fyle_rest_auth	authtoken
7	users	user
8	bamboohr	bamboohr
10	orgs	org
11	orgs	fylecredential
9	bamboohr	bamboohrconfiguration
12	travelperk	travelperk
13	travelperk	travelperkconfiguration
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	users	0001_initial	2022-12-06 14:32:18.022273+05:30
2	contenttypes	0001_initial	2022-12-06 14:32:18.034756+05:30
3	admin	0001_initial	2022-12-06 14:32:18.048041+05:30
4	admin	0002_logentry_remove_auto_add	2022-12-06 14:32:18.065884+05:30
5	admin	0003_logentry_add_action_flag_choices	2022-12-06 14:32:18.069645+05:30
6	contenttypes	0002_remove_content_type_name	2022-12-06 14:32:18.081797+05:30
7	auth	0001_initial	2022-12-06 14:32:18.10736+05:30
8	auth	0002_alter_permission_name_max_length	2022-12-06 14:32:18.134234+05:30
9	auth	0003_alter_user_email_max_length	2022-12-06 14:32:18.138514+05:30
10	auth	0004_alter_user_username_opts	2022-12-06 14:32:18.142935+05:30
11	auth	0005_alter_user_last_login_null	2022-12-06 14:32:18.148892+05:30
12	auth	0006_require_contenttypes_0002	2022-12-06 14:32:18.151058+05:30
13	auth	0007_alter_validators_add_error_messages	2022-12-06 14:32:18.155629+05:30
14	auth	0008_alter_user_username_max_length	2022-12-06 14:32:18.16014+05:30
15	auth	0009_alter_user_last_name_max_length	2022-12-06 14:32:18.164688+05:30
16	auth	0010_alter_group_name_max_length	2022-12-06 14:32:18.174758+05:30
17	auth	0011_update_proxy_permissions	2022-12-06 14:32:18.180157+05:30
18	auth	0012_alter_user_first_name_max_length	2022-12-06 14:32:18.184402+05:30
19	orgs	0001_initial	2022-12-06 14:32:18.215468+05:30
20	bamboohr	0001_initial	2022-12-06 14:32:18.246728+05:30
21	bamboohr	0002_configuration	2022-12-06 14:32:18.264679+05:30
22	fyle_rest_auth	0001_initial	2022-12-06 14:32:18.28398+05:30
23	fyle_rest_auth	0002_auto_20200101_1205	2022-12-06 14:32:18.346245+05:30
24	fyle_rest_auth	0003_auto_20200107_0921	2022-12-06 14:32:18.363352+05:30
25	fyle_rest_auth	0004_auto_20200107_1345	2022-12-06 14:32:18.37859+05:30
26	fyle_rest_auth	0005_remove_authtoken_access_token	2022-12-06 14:32:18.383442+05:30
27	fyle_rest_auth	0006_auto_20201221_0849	2022-12-06 14:32:18.388297+05:30
28	sessions	0001_initial	2022-12-06 14:32:18.39665+05:30
29	bamboohr	0003_auto_20221212_1052	2022-12-19 17:31:54.513271+05:30
30	orgs	0002_auto_20221219_1044	2022-12-19 17:31:54.528076+05:30
31	bamboohr	0004_auto_20221220_0935	2022-12-21 01:31:46.786736+05:30
32	travelperk	0001_initial	2023-01-23 15:54:48.169439+05:30
33	travelperk	0002_travelperk_travelperk_connection_id	2023-03-16 13:40:10.326912+05:30
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
1	Fyle For NetSuite Projects Customers	orf7jLXaJ6SY	12312	https://staging.fyle.tech	2022-12-06 14:37:20.620757+05:30	2022-12-06 14:38:17.03424+05:30	\N	\N
\.


--
-- Data for Name: orgs_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orgs_user (id, org_id, user_id) FROM stdin;
1	1	1
\.


--
-- Data for Name: travelperk; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.travelperk (id, folder_id, package_id, is_fyle_connected, is_s3_connected, created_at, updated_at, org_id, travelperk_connection_id) FROM stdin;
8	162	111	\N	\N	2022-12-06 14:42:38.724679+05:30	2022-12-06 14:43:33.008685+05:30	1	\N
\.


--
-- Data for Name: travelperk_configurations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.travelperk_configurations (id, recipe_id, recipe_data, is_recipe_enabled, org_id) FROM stdin;
2	3429	{"number": 0, "provider": "bamboohr", "name": "updated_employee", "as": "6761c014", "title": null, "description": null, "keyword": "trigger", "dynamicPickListSelection": {}, "toggleCfg": {"flag": true}, "input": {"flag": "true"}, "extended_output_schema": [{"control_type": "text", "label": "NIN", "name": "customNIN1", "optional": true, "type": "string"}, {"control_type": "select", "label": "Secondary Language", "name": "customSecondaryLanguage1", "optional": true, "pick_list": [["French", "French"], ["German", "German"], ["Japanese", "Japanese"], ["Mandarin", "Mandarin"], ["Spanish", "Spanish"]], "toggle_field": {"control_type": "text", "label": "Secondary Language", "toggle_hint": "Enter custom value", "optional": true, "type": "string", "name": "customSecondaryLanguage1"}, "toggle_hint": "Select from list", "type": "string"}, {"control_type": "select", "label": "Shirt size", "name": "customShirtsize", "optional": true, "pick_list": [["1. Small", "1. Small"], ["2. Medium", "2. Medium"], ["3. Large", "3. Large"], ["4. XLarge", "4. XLarge"], ["5. XXLarge", "5. XXLarge"]], "toggle_field": {"control_type": "text", "label": "Shirt size", "toggle_hint": "Enter custom value", "optional": true, "type": "string", "name": "customShirtsize"}, "toggle_hint": "Select from list", "type": "string"}, {"control_type": "text", "label": "Tax File Number", "name": "customTaxFileNumber1", "optional": true, "type": "string"}], "block": [{"number": 1, "keyword": "try", "dynamicPickListSelection": {}, "toggleCfg": {}, "input": {}, "block": [{"number": 2, "keyword": "if", "dynamicPickListSelection": {}, "toggleCfg": {}, "input": {"type": "compound", "operand": "and", "conditions": [{"operand": "present", "lhs": "#{_('data.bamboohr.6761c014.supervisorEId')}", "rhs": "", "uuid": "condition-79dc736e-21b3-4f53-bcd3-eafef8a76362"}]}, "block": [{"number": 3, "provider": "bamboohr", "name": "get_employee_by_id", "as": "e5cf843b", "title": null, "description": null, "keyword": "action", "dynamicPickListSelection": {}, "toggleCfg": {}, "input": {"id": "#{_('data.bamboohr.6761c014.supervisorEId')}"}, "extended_output_schema": [{"control_type": "text", "label": "NIN", "name": "customNIN1", "optional": true, "type": "string"}, {"control_type": "select", "label": "Secondary Language", "name": "customSecondaryLanguage1", "optional": true, "pick_list": [["French", "French"], ["German", "German"], ["Japanese", "Japanese"], ["Mandarin", "Mandarin"], ["Spanish", "Spanish"]], "toggle_field": {"control_type": "text", "label": "Secondary Language", "toggle_hint": "Enter custom value", "optional": true, "type": "string", "name": "customSecondaryLanguage1"}, "toggle_hint": "Select from list", "type": "string"}, {"control_type": "select", "label": "Shirt size", "name": "customShirtsize", "optional": true, "pick_list": [["1. Small", "1. Small"], ["2. Medium", "2. Medium"], ["3. Large", "3. Large"], ["4. XLarge", "4. XLarge"], ["5. XXLarge", "5. XXLarge"]], "toggle_field": {"control_type": "text", "label": "Shirt size", "toggle_hint": "Enter custom value", "optional": true, "type": "string", "name": "customShirtsize"}, "toggle_hint": "Select from list", "type": "string"}, {"control_type": "text", "label": "Tax File Number", "name": "customTaxFileNumber1", "optional": true, "type": "string"}], "uuid": "587d07c1-2d4e-473a-853a-f768b441bd7c"}, {"number": 4, "provider": "fyle_staging_connector_892703_1670317976", "name": "search_employee", "as": "d02a328f", "title": null, "description": null, "keyword": "action", "dynamicPickListSelection": {}, "toggleCfg": {}, "input": {"email": "='eq.' + _('data.bamboohr.e5cf843b.workEmail')"}, "extended_output_schema": [{"label": "Employees", "name": "data", "of": "object", "optional": true, "properties": [{"control_type": "number", "label": "Count", "parse_output": "float_conversion", "optional": true, "type": "number", "name": "count"}, {"name": "data", "type": "array", "of": "object", "label": "Data", "optional": true, "properties": [{"control_type": "text", "label": "Branch account", "optional": true, "type": "string", "name": "branch_account"}, {"control_type": "text", "label": "Branch ifsc", "optional": true, "type": "string", "name": "branch_ifsc"}, {"control_type": "text", "label": "Business unit", "optional": true, "type": "string", "name": "business_unit"}, {"control_type": "text", "label": "Code", "optional": true, "type": "string", "name": "code"}, {"control_type": "text", "label": "Created at", "render_input": "date_time_conversion", "parse_output": "date_time_conversion", "optional": true, "type": "date_time", "name": "created_at"}, {"control_type": "text", "label": "Department", "optional": true, "type": "string", "name": "department"}, {"control_type": "text", "label": "Department ID", "optional": true, "type": "string", "name": "department_id"}, {"control_type": "text", "label": "Has accepted invite", "parse_output": {}, "render_input": {}, "toggle_hint": "Select from option list", "toggle_field": {"label": "Has accepted invite", "control_type": "text", "toggle_hint": "Use custom value", "type": "boolean", "name": "has_accepted_invite"}, "optional": true, "type": "number", "name": "has_accepted_invite"}, {"control_type": "text", "label": "ID", "optional": true, "type": "string", "name": "id"}, {"control_type": "text", "label": "Is enabled", "parse_output": {}, "render_input": {}, "toggle_hint": "Select from option list", "toggle_field": {"label": "Is enabled", "control_type": "text", "toggle_hint": "Use custom value", "type": "boolean", "name": "is_enabled"}, "optional": true, "type": "number", "name": "is_enabled"}, {"control_type": "text", "label": "Joined at", "render_input": "date_time_conversion", "parse_output": "date_time_conversion", "optional": true, "type": "date_time", "name": "joined_at"}, {"control_type": "text", "label": "Level", "optional": true, "type": "string", "name": "level"}, {"control_type": "text", "label": "Level ID", "optional": true, "type": "string", "name": "level_id"}, {"control_type": "text", "label": "Location", "optional": true, "type": "string", "name": "location"}, {"control_type": "text", "label": "Mobile", "optional": true, "type": "string", "name": "mobile"}, {"control_type": "text", "label": "Org ID", "optional": true, "type": "string", "name": "org_id"}, {"name": "roles", "type": "array", "of": "string", "label": "Roles", "optional": true}, {"control_type": "text", "label": "Special email", "optional": true, "type": "string", "name": "special_email"}, {"control_type": "text", "label": "Title", "optional": true, "type": "string", "name": "title"}, {"control_type": "text", "label": "Updated at", "render_input": "date_time_conversion", "parse_output": "date_time_conversion", "optional": true, "type": "date_time", "name": "updated_at"}, {"label": "User", "optional": true, "type": "object", "name": "user", "properties": [{"control_type": "text", "label": "Email", "optional": true, "type": "string", "name": "email"}, {"control_type": "text", "label": "Full name", "optional": true, "type": "string", "name": "full_name"}, {"control_type": "text", "label": "ID", "optional": true, "type": "string", "name": "id"}]}, {"control_type": "text", "label": "User ID", "optional": true, "type": "string", "name": "user_id"}]}, {"control_type": "number", "label": "Offset", "parse_output": "float_conversion", "optional": true, "type": "number", "name": "offset"}], "type": "array"}], "uuid": "55913e43-d3fd-451e-837a-445246be5c7f"}], "uuid": "499d0a9a-7aec-4b07-a106-30ca7589545a"}, {"number": 5, "provider": "fyle_staging_connector_892703_1670317976", "name": "create_employees_in_fyle", "as": "07f04431", "title": null, "description": null, "keyword": "action", "dynamicPickListSelection": {}, "toggleCfg": {}, "input": {"data": {"user_email": "#{_('data.bamboohr.6761c014.workEmail')}", "user_full_name": "#{_('data.bamboohr.6761c014.displayName')}", "title": "#{_('data.bamboohr.6761c014.jobTitle')}", "location": "#{_('data.bamboohr.6761c014.location')}", "is_enabled": "=_('data.bamboohr.6761c014.status').include?(\\"Active\\")", "approver_emails": "=_('data.fyle_staging_connector_892703_1670317976.d02a328f.data').present? ? [_('data.bamboohr.e5cf843b.workEmail')] : []"}}, "visible_config_fields": ["data", "data.is_enabled", "data.user_full_name", "data.user_email", "data.title", "data.location", "data.approver_emails"], "uuid": "36320f70-4509-46fe-80c3-fd89ac93a0dd", "skip": false}, {"number": 6, "as": "86be96e2", "keyword": "catch", "dynamicPickListSelection": {}, "toggleCfg": {}, "input": {"max_retry_count": "0", "retry_interval": "2"}, "block": [{"number": 7, "provider": "sendgrid", "name": "send_email", "as": "2c55fabe", "keyword": "action", "dynamicPickListSelection": {}, "toggleCfg": {}, "input": {"personalizations": {"to": {"email": "ni12lesh[amt1212@gmail.in"}}, "from": {"email": "notifications-staging@fylehq.com"}, "subject": "This Is A Test Email", "content": {"type": "text/plain", "value": "This is a Test Email From Workato"}}, "uuid": "93f8d230-00ae-456e-891c-653daa656dea"}], "uuid": "d6e76e57-08a2-4d26-a7c1-d74c92709d06"}], "uuid": "14f5a93e-8d8a-4659-8dba-ded9b816b173"}], "uuid": "9facdee0-dff2-4a3c-bf60-06265ca8a599"}	f	1
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (password, last_login, id, email, user_id, full_name, active, staff, admin) FROM stdin;
	\N	1	ashwin.t+123@fyle.in	usqywo0fBY		t	f	f
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

SELECT pg_catalog.setval('public.auth_permission_id_seq', 56, true);


--
-- Name: bamboohr_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.bamboohr_id_seq', 1, true);


--
-- Name: configurations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.configurations_id_seq', 1, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 13, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 33, true);


--
-- Name: fyle_credentials_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.fyle_credentials_id_seq', 1, true);


--
-- Name: fyle_rest_auth_authtokens_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.fyle_rest_auth_authtokens_id_seq', 1, true);


--
-- Name: orgs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orgs_id_seq', 1, true);


--
-- Name: orgs_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.orgs_user_id_seq', 1, true);


--
-- Name: travelperk_configurations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.travelperk_configurations_id_seq', 1, false);


--
-- Name: travelperk_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.travelperk_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 1, true);


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
-- Name: bamboohr_configurations configurations_org_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bamboohr_configurations
    ADD CONSTRAINT configurations_org_id_key UNIQUE (org_id);


--
-- Name: bamboohr_configurations configurations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bamboohr_configurations
    ADD CONSTRAINT configurations_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


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
-- Name: travelperk_configurations travelperk_configurations_org_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.travelperk_configurations
    ADD CONSTRAINT travelperk_configurations_org_id_key UNIQUE (org_id);


--
-- Name: travelperk_configurations travelperk_configurations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.travelperk_configurations
    ADD CONSTRAINT travelperk_configurations_pkey PRIMARY KEY (id);


--
-- Name: travelperk travelperk_org_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.travelperk
    ADD CONSTRAINT travelperk_org_id_key UNIQUE (org_id);


--
-- Name: travelperk travelperk_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.travelperk
    ADD CONSTRAINT travelperk_pkey PRIMARY KEY (id);


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
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


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
-- Name: bamboohr_configurations configurations_org_id_ddcda5f1_fk_orgs_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.bamboohr_configurations
    ADD CONSTRAINT configurations_org_id_ddcda5f1_fk_orgs_id FOREIGN KEY (org_id) REFERENCES public.orgs(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_users_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_users_id FOREIGN KEY (user_id) REFERENCES public.users(id) DEFERRABLE INITIALLY DEFERRED;


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
-- Name: travelperk_configurations travelperk_configurations_org_id_2c88713e_fk_orgs_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.travelperk_configurations
    ADD CONSTRAINT travelperk_configurations_org_id_2c88713e_fk_orgs_id FOREIGN KEY (org_id) REFERENCES public.orgs(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: travelperk travelperk_org_id_fb977dc7_fk_orgs_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.travelperk
    ADD CONSTRAINT travelperk_org_id_fb977dc7_fk_orgs_id FOREIGN KEY (org_id) REFERENCES public.orgs(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

