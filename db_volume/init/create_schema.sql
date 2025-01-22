--
-- PostgreSQL database dump
--

-- Dumped from database version 14.15 (Postgres.app)
-- Dumped by pg_dump version 14.13 (Homebrew)

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

ALTER TABLE public.auth_group ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.auth_group_permissions (
    id bigint NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.auth_group_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


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

ALTER TABLE public.auth_permission ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: authtoken_token; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.authtoken_token (
    key character varying(40) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.authtoken_token OWNER TO postgres;

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
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_admin_log ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


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

ALTER TABLE public.django_content_type ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.django_migrations (
    id bigint NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.django_migrations ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


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
-- Name: item_store_basket; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_store_basket (
    id bigint NOT NULL,
    quantity integer NOT NULL,
    customer_id bigint NOT NULL,
    product_id bigint NOT NULL
);


ALTER TABLE public.item_store_basket OWNER TO postgres;

--
-- Name: item_store_basket_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.item_store_basket ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.item_store_basket_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: item_store_customer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_store_customer (
    id bigint NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    first_name character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    username text NOT NULL,
    password text NOT NULL,
    email character varying(100) NOT NULL,
    total_basket_cost numeric(30,2) NOT NULL
);


ALTER TABLE public.item_store_customer OWNER TO postgres;

--
-- Name: item_store_customer_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_store_customer_groups (
    id bigint NOT NULL,
    customer_id bigint NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.item_store_customer_groups OWNER TO postgres;

--
-- Name: item_store_customer_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.item_store_customer_groups ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.item_store_customer_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: item_store_customer_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.item_store_customer ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.item_store_customer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: item_store_customer_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_store_customer_user_permissions (
    id bigint NOT NULL,
    customer_id bigint NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.item_store_customer_user_permissions OWNER TO postgres;

--
-- Name: item_store_customer_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.item_store_customer_user_permissions ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.item_store_customer_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: item_store_order; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_store_order (
    id bigint NOT NULL,
    quantity integer NOT NULL,
    product_id bigint NOT NULL,
    order_number_id bigint
);


ALTER TABLE public.item_store_order OWNER TO postgres;

--
-- Name: item_store_order_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.item_store_order ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.item_store_order_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: item_store_ordernumber; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_store_ordernumber (
    id bigint NOT NULL,
    date date NOT NULL,
    customer_id bigint NOT NULL,
    total_cost numeric(30,2) NOT NULL
);


ALTER TABLE public.item_store_ordernumber OWNER TO postgres;

--
-- Name: item_store_ordernumber_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.item_store_ordernumber ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.item_store_ordernumber_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: item_store_review; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.item_store_review (
    id bigint NOT NULL,
    rating integer NOT NULL,
    comment text NOT NULL,
    customer_id bigint NOT NULL,
    product_id bigint NOT NULL,
    CONSTRAINT item_store_review_rating_check CHECK ((rating >= 0))
);


ALTER TABLE public.item_store_review OWNER TO postgres;

--
-- Name: item_store_review_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.item_store_review ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.item_store_review_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: products_product; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products_product (
    id bigint NOT NULL,
    name character varying(40) NOT NULL,
    price numeric(30,2) NOT NULL,
    stock smallint NOT NULL,
    CONSTRAINT products_product_stock_check CHECK ((stock >= 0))
);


ALTER TABLE public.products_product OWNER TO postgres;

--
-- Name: products_product_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.products_product ALTER COLUMN id ADD GENERATED BY DEFAULT AS IDENTITY (
    SEQUENCE NAME public.products_product_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


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
21	Can add Token	6	add_token
22	Can change Token	6	change_token
23	Can delete Token	6	delete_token
24	Can view Token	6	view_token
25	Can add Token	7	add_tokenproxy
26	Can change Token	7	change_tokenproxy
27	Can delete Token	7	delete_tokenproxy
28	Can view Token	7	view_tokenproxy
29	Can add Customer	8	add_customer
30	Can change Customer	8	change_customer
31	Can delete Customer	8	delete_customer
32	Can view Customer	8	view_customer
33	Can add review	9	add_review
34	Can change review	9	change_review
35	Can delete review	9	delete_review
36	Can view review	9	view_review
37	Can add order	10	add_order
38	Can change order	10	change_order
39	Can delete order	10	delete_order
40	Can view order	10	view_order
41	Can add basket	11	add_basket
42	Can change basket	11	change_basket
43	Can delete basket	11	delete_basket
44	Can view basket	11	view_basket
45	Can add order number	12	add_ordernumber
46	Can change order number	12	change_ordernumber
47	Can delete order number	12	delete_ordernumber
48	Can view order number	12	view_ordernumber
49	Can add product	13	add_product
50	Can change product	13	change_product
51	Can delete product	13	delete_product
52	Can view product	13	view_product
\.


--
-- Data for Name: authtoken_token; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.authtoken_token (key, created, user_id) FROM stdin;
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
6	authtoken	token
7	authtoken	tokenproxy
8	item_store	customer
9	item_store	review
10	item_store	order
11	item_store	basket
12	item_store	ordernumber
13	products	product
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	products	0001_initial	2025-01-19 13:27:49.595453+00
2	contenttypes	0001_initial	2025-01-19 13:27:49.608087+00
3	contenttypes	0002_remove_content_type_name	2025-01-19 13:27:49.62017+00
4	auth	0001_initial	2025-01-19 13:27:49.668901+00
5	auth	0002_alter_permission_name_max_length	2025-01-19 13:27:49.684748+00
6	auth	0003_alter_user_email_max_length	2025-01-19 13:27:49.693761+00
7	auth	0004_alter_user_username_opts	2025-01-19 13:27:49.704255+00
8	auth	0005_alter_user_last_login_null	2025-01-19 13:27:49.714754+00
9	auth	0006_require_contenttypes_0002	2025-01-19 13:27:49.716902+00
10	auth	0007_alter_validators_add_error_messages	2025-01-19 13:27:49.726415+00
11	auth	0008_alter_user_username_max_length	2025-01-19 13:27:49.735635+00
12	auth	0009_alter_user_last_name_max_length	2025-01-19 13:27:49.746878+00
13	auth	0010_alter_group_name_max_length	2025-01-19 13:27:49.756768+00
14	auth	0011_update_proxy_permissions	2025-01-19 13:27:49.76634+00
15	auth	0012_alter_user_first_name_max_length	2025-01-19 13:27:49.774049+00
16	item_store	0001_initial	2025-01-19 13:27:49.878591+00
17	admin	0001_initial	2025-01-19 13:27:49.898881+00
18	admin	0002_logentry_remove_auto_add	2025-01-19 13:27:49.90963+00
19	admin	0003_logentry_add_action_flag_choices	2025-01-19 13:27:49.921099+00
20	authtoken	0001_initial	2025-01-19 13:27:49.938872+00
21	authtoken	0002_auto_20160226_1747	2025-01-19 13:27:49.981905+00
22	authtoken	0003_tokenproxy	2025-01-19 13:27:49.984286+00
23	authtoken	0004_alter_tokenproxy_options	2025-01-19 13:27:49.988539+00
24	item_store	0002_alter_customer_email	2025-01-19 13:27:50.008731+00
25	item_store	0003_rename_products_basket_product_alter_basket_quantity_and_more	2025-01-19 13:27:50.06576+00
26	item_store	0004_alter_basket_quantity_alter_customer_email_and_more	2025-01-19 13:27:50.120868+00
27	item_store	0005_remove_order_customer_remove_order_date_and_more	2025-01-19 13:27:50.176061+00
28	item_store	0006_alter_order_order_number_alter_review_customer_and_more	2025-01-19 13:27:50.249907+00
29	item_store	0007_alter_basket_customer_alter_basket_unique_together_and_more	2025-01-19 13:27:50.297148+00
30	item_store	0008_alter_customer_email	2025-01-19 13:27:50.311081+00
31	item_store	0009_remove_ordernumber_status	2025-01-19 13:27:50.322558+00
32	item_store	0010_customer_total_basket_cost_ordernumber_total_cost	2025-01-19 13:27:50.34893+00
33	item_store	0011_alter_customer_total_basket_cost_and_more	2025-01-19 13:27:50.371386+00
34	products	0002_alter_product_price	2025-01-19 13:27:50.378363+00
35	products	0003_remove_product_type	2025-01-19 13:27:50.38382+00
36	sessions	0001_initial	2025-01-19 13:27:50.394345+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: item_store_basket; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_store_basket (id, quantity, customer_id, product_id) FROM stdin;
\.


--
-- Data for Name: item_store_customer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_store_customer (id, last_login, is_superuser, first_name, last_name, is_staff, is_active, date_joined, username, password, email, total_basket_cost) FROM stdin;
\.


--
-- Data for Name: item_store_customer_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_store_customer_groups (id, customer_id, group_id) FROM stdin;
\.


--
-- Data for Name: item_store_customer_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_store_customer_user_permissions (id, customer_id, permission_id) FROM stdin;
\.


--
-- Data for Name: item_store_order; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_store_order (id, quantity, product_id, order_number_id) FROM stdin;
\.


--
-- Data for Name: item_store_ordernumber; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_store_ordernumber (id, date, customer_id, total_cost) FROM stdin;
\.


--
-- Data for Name: item_store_review; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.item_store_review (id, rating, comment, customer_id, product_id) FROM stdin;
\.


--
-- Data for Name: products_product; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.products_product (id, name, price, stock) FROM stdin;
5	Crayons	1.20	500
204	Blue Shirt	5.90	467
4	Mouse	10.00	399
205	Red Shoes	3.55	214
206	Green Jacket	3.50	350
207	Black Pants	4.81	131
208	White Dress	5.42	263
209	Yellow Hat	3.26	198
210	Purple Scarf	5.11	254
211	Orange Sweater	3.88	416
212	Pink Skirt	2.30	420
213	Brown Boots	5.54	129
215	Beige Blouse	4.67	480
217	Maroon T-shirt	0.53	446
219	Gold Earrings	4.15	277
220	Silver Bracelet	7.79	191
221	Coral Necklace	8.34	174
222	Magenta Gloves	5.41	59
216	Navy Jeans	6.18	19
214	Gray Coat	8.06	163
218	Teal Socks	4.30	245
223	Turquoise Belt	3.54	232
3	pencil	3.00	424
1	Book	5.50	438
2	Pen	3.00	478
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

SELECT pg_catalog.setval('public.auth_permission_id_seq', 52, true);


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

SELECT pg_catalog.setval('public.django_migrations_id_seq', 36, true);


--
-- Name: item_store_basket_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_store_basket_id_seq', 3, true);


--
-- Name: item_store_customer_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_store_customer_groups_id_seq', 1, false);


--
-- Name: item_store_customer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_store_customer_id_seq', 2, true);


--
-- Name: item_store_customer_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_store_customer_user_permissions_id_seq', 1, false);


--
-- Name: item_store_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_store_order_id_seq', 2, true);


--
-- Name: item_store_ordernumber_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_store_ordernumber_id_seq', 1, true);


--
-- Name: item_store_review_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.item_store_review_id_seq', 14, true);


--
-- Name: products_product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.products_product_id_seq', 1, false);


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
-- Name: authtoken_token authtoken_token_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_pkey PRIMARY KEY (key);


--
-- Name: authtoken_token authtoken_token_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_key UNIQUE (user_id);


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
-- Name: item_store_basket item_store_basket_customer_id_product_id_d26e317e_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_store_basket
    ADD CONSTRAINT item_store_basket_customer_id_product_id_d26e317e_uniq UNIQUE (customer_id, product_id);


--
-- Name: item_store_basket item_store_basket_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_store_basket
    ADD CONSTRAINT item_store_basket_pkey PRIMARY KEY (id);


--
-- Name: item_store_customer item_store_customer_email_a465371c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_store_customer
    ADD CONSTRAINT item_store_customer_email_a465371c_uniq UNIQUE (email);


--
-- Name: item_store_customer_groups item_store_customer_groups_customer_id_group_id_068a7e05_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_store_customer_groups
    ADD CONSTRAINT item_store_customer_groups_customer_id_group_id_068a7e05_uniq UNIQUE (customer_id, group_id);


--
-- Name: item_store_customer_groups item_store_customer_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_store_customer_groups
    ADD CONSTRAINT item_store_customer_groups_pkey PRIMARY KEY (id);


--
-- Name: item_store_customer item_store_customer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_store_customer
    ADD CONSTRAINT item_store_customer_pkey PRIMARY KEY (id);


--
-- Name: item_store_customer_user_permissions item_store_customer_user_customer_id_permission_i_a336e202_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_store_customer_user_permissions
    ADD CONSTRAINT item_store_customer_user_customer_id_permission_i_a336e202_uniq UNIQUE (customer_id, permission_id);


--
-- Name: item_store_customer_user_permissions item_store_customer_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_store_customer_user_permissions
    ADD CONSTRAINT item_store_customer_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: item_store_customer item_store_customer_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_store_customer
    ADD CONSTRAINT item_store_customer_username_key UNIQUE (username);


--
-- Name: item_store_order item_store_order_order_number_id_product_id_e0741138_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_store_order
    ADD CONSTRAINT item_store_order_order_number_id_product_id_e0741138_uniq UNIQUE (order_number_id, product_id);


--
-- Name: item_store_order item_store_order_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_store_order
    ADD CONSTRAINT item_store_order_pkey PRIMARY KEY (id);


--
-- Name: item_store_ordernumber item_store_ordernumber_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_store_ordernumber
    ADD CONSTRAINT item_store_ordernumber_pkey PRIMARY KEY (id);


--
-- Name: item_store_review item_store_review_customer_id_product_id_87db3e12_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_store_review
    ADD CONSTRAINT item_store_review_customer_id_product_id_87db3e12_uniq UNIQUE (customer_id, product_id);


--
-- Name: item_store_review item_store_review_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_store_review
    ADD CONSTRAINT item_store_review_pkey PRIMARY KEY (id);


--
-- Name: products_product products_product_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products_product
    ADD CONSTRAINT products_product_pkey PRIMARY KEY (id);


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
-- Name: authtoken_token_key_10f0b77e_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX authtoken_token_key_10f0b77e_like ON public.authtoken_token USING btree (key varchar_pattern_ops);


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
-- Name: item_store_basket_customer_id_cc74653d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX item_store_basket_customer_id_cc74653d ON public.item_store_basket USING btree (customer_id);


--
-- Name: item_store_basket_products_id_dda0e57e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX item_store_basket_products_id_dda0e57e ON public.item_store_basket USING btree (product_id);


--
-- Name: item_store_customer_email_a465371c_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX item_store_customer_email_a465371c_like ON public.item_store_customer USING btree (email varchar_pattern_ops);


--
-- Name: item_store_customer_groups_customer_id_1087fcdd; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX item_store_customer_groups_customer_id_1087fcdd ON public.item_store_customer_groups USING btree (customer_id);


--
-- Name: item_store_customer_groups_group_id_c3a09771; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX item_store_customer_groups_group_id_c3a09771 ON public.item_store_customer_groups USING btree (group_id);


--
-- Name: item_store_customer_user_permissions_customer_id_3e228350; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX item_store_customer_user_permissions_customer_id_3e228350 ON public.item_store_customer_user_permissions USING btree (customer_id);


--
-- Name: item_store_customer_user_permissions_permission_id_dc23fc24; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX item_store_customer_user_permissions_permission_id_dc23fc24 ON public.item_store_customer_user_permissions USING btree (permission_id);


--
-- Name: item_store_customer_username_b3695e06_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX item_store_customer_username_b3695e06_like ON public.item_store_customer USING btree (username text_pattern_ops);


--
-- Name: item_store_order_order_number_id_8f0cff32; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX item_store_order_order_number_id_8f0cff32 ON public.item_store_order USING btree (order_number_id);


--
-- Name: item_store_order_product_id_a129d8a0; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX item_store_order_product_id_a129d8a0 ON public.item_store_order USING btree (product_id);


--
-- Name: item_store_ordernumber_customer_id_dfd10a89; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX item_store_ordernumber_customer_id_dfd10a89 ON public.item_store_ordernumber USING btree (customer_id);


--
-- Name: item_store_review_customer_id_9b6991ca; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX item_store_review_customer_id_9b6991ca ON public.item_store_review USING btree (customer_id);


--
-- Name: item_store_review_product_id_bda05a6e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX item_store_review_product_id_bda05a6e ON public.item_store_review USING btree (product_id);


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
-- Name: authtoken_token authtoken_token_user_id_35299eff_fk_item_store_customer_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_35299eff_fk_item_store_customer_id FOREIGN KEY (user_id) REFERENCES public.item_store_customer(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_item_store_customer_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_item_store_customer_id FOREIGN KEY (user_id) REFERENCES public.item_store_customer(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: item_store_basket item_store_basket_customer_id_cc74653d_fk_item_stor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_store_basket
    ADD CONSTRAINT item_store_basket_customer_id_cc74653d_fk_item_stor FOREIGN KEY (customer_id) REFERENCES public.item_store_customer(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: item_store_basket item_store_basket_product_id_f6d8600d_fk_products_product_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_store_basket
    ADD CONSTRAINT item_store_basket_product_id_f6d8600d_fk_products_product_id FOREIGN KEY (product_id) REFERENCES public.products_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: item_store_customer_groups item_store_customer__customer_id_1087fcdd_fk_item_stor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_store_customer_groups
    ADD CONSTRAINT item_store_customer__customer_id_1087fcdd_fk_item_stor FOREIGN KEY (customer_id) REFERENCES public.item_store_customer(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: item_store_customer_user_permissions item_store_customer__customer_id_3e228350_fk_item_stor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_store_customer_user_permissions
    ADD CONSTRAINT item_store_customer__customer_id_3e228350_fk_item_stor FOREIGN KEY (customer_id) REFERENCES public.item_store_customer(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: item_store_customer_user_permissions item_store_customer__permission_id_dc23fc24_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_store_customer_user_permissions
    ADD CONSTRAINT item_store_customer__permission_id_dc23fc24_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: item_store_customer_groups item_store_customer_groups_group_id_c3a09771_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_store_customer_groups
    ADD CONSTRAINT item_store_customer_groups_group_id_c3a09771_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: item_store_order item_store_order_order_number_id_8f0cff32_fk_item_stor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_store_order
    ADD CONSTRAINT item_store_order_order_number_id_8f0cff32_fk_item_stor FOREIGN KEY (order_number_id) REFERENCES public.item_store_ordernumber(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: item_store_order item_store_order_product_id_a129d8a0_fk_products_product_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_store_order
    ADD CONSTRAINT item_store_order_product_id_a129d8a0_fk_products_product_id FOREIGN KEY (product_id) REFERENCES public.products_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: item_store_ordernumber item_store_ordernumb_customer_id_dfd10a89_fk_item_stor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_store_ordernumber
    ADD CONSTRAINT item_store_ordernumb_customer_id_dfd10a89_fk_item_stor FOREIGN KEY (customer_id) REFERENCES public.item_store_customer(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: item_store_review item_store_review_customer_id_9b6991ca_fk_item_stor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_store_review
    ADD CONSTRAINT item_store_review_customer_id_9b6991ca_fk_item_stor FOREIGN KEY (customer_id) REFERENCES public.item_store_customer(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: item_store_review item_store_review_product_id_bda05a6e_fk_products_product_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.item_store_review
    ADD CONSTRAINT item_store_review_product_id_bda05a6e_fk_products_product_id FOREIGN KEY (product_id) REFERENCES public.products_product(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

