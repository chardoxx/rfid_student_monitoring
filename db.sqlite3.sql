BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "attendance_app_attendancerecord" (
	"id"	integer NOT NULL,
	"date"	date NOT NULL,
	"time_in"	time,
	"time_out"	time,
	"status"	varchar(10) NOT NULL,
	"photo"	varchar(100),
	"created_at"	datetime NOT NULL,
	"student_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("student_id") REFERENCES "attendance_app_student"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "attendance_app_course" (
	"id"	integer NOT NULL,
	"code"	varchar(20) NOT NULL UNIQUE,
	"name"	varchar(100) NOT NULL,
	"description"	text,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "attendance_app_emailsettings" (
	"id"	integer NOT NULL,
	"time_in_subject"	varchar(100) NOT NULL,
	"time_in_template"	text NOT NULL,
	"time_out_subject"	varchar(100) NOT NULL,
	"time_out_template"	text NOT NULL,
	"smtp_host"	varchar(100) NOT NULL,
	"smtp_port"	integer NOT NULL,
	"smtp_username"	varchar(100) NOT NULL,
	"smtp_password"	varchar(100) NOT NULL,
	"from_email"	varchar(254) NOT NULL,
	"from_name"	varchar(100) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "attendance_app_section" (
	"id"	integer NOT NULL,
	"name"	varchar(50) NOT NULL,
	"year_level"	integer NOT NULL,
	"course_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("course_id") REFERENCES "attendance_app_course"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "attendance_app_student" (
	"id"	integer NOT NULL,
	"student_id"	varchar(20) NOT NULL UNIQUE,
	"rfid_tag"	varchar(50) UNIQUE,
	"first_name"	varchar(50) NOT NULL,
	"last_name"	varchar(50) NOT NULL,
	"birthday"	date,
	"gender"	varchar(1),
	"year_level"	integer NOT NULL,
	"email"	varchar(254),
	"address"	text,
	"guardian_name"	varchar(100),
	"guardian_email"	varchar(254),
	"photo"	varchar(100),
	"created_at"	datetime NOT NULL,
	"updated_at"	datetime NOT NULL,
	"section_id"	bigint NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("section_id") REFERENCES "attendance_app_section"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "attendance_app_systemlog" (
	"id"	integer NOT NULL,
	"timestamp"	datetime NOT NULL,
	"log_type"	varchar(10) NOT NULL,
	"message"	text NOT NULL,
	"details"	text,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "attendance_app_systemsettings" (
	"id"	integer NOT NULL,
	"system_title"	varchar(100) NOT NULL,
	"footer_text"	varchar(100) NOT NULL,
	"logo"	varchar(100),
	"version"	varchar(20) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_group" (
	"id"	integer NOT NULL,
	"name"	varchar(150) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" (
	"id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_permission" (
	"id"	integer NOT NULL,
	"content_type_id"	integer NOT NULL,
	"codename"	varchar(100) NOT NULL,
	"name"	varchar(255) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_user" (
	"id"	integer NOT NULL,
	"password"	varchar(128) NOT NULL,
	"last_login"	datetime,
	"is_superuser"	bool NOT NULL,
	"username"	varchar(150) NOT NULL UNIQUE,
	"last_name"	varchar(150) NOT NULL,
	"email"	varchar(254) NOT NULL,
	"is_staff"	bool NOT NULL,
	"is_active"	bool NOT NULL,
	"date_joined"	datetime NOT NULL,
	"first_name"	varchar(150) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_user_groups" (
	"id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "auth_user_user_permissions" (
	"id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_admin_log" (
	"id"	integer NOT NULL,
	"object_id"	text,
	"object_repr"	varchar(200) NOT NULL,
	"action_flag"	smallint unsigned NOT NULL CHECK("action_flag" >= 0),
	"change_message"	text NOT NULL,
	"content_type_id"	integer,
	"user_id"	integer NOT NULL,
	"action_time"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED
);
CREATE TABLE IF NOT EXISTS "django_content_type" (
	"id"	integer NOT NULL,
	"app_label"	varchar(100) NOT NULL,
	"model"	varchar(100) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "django_migrations" (
	"id"	integer NOT NULL,
	"app"	varchar(255) NOT NULL,
	"name"	varchar(255) NOT NULL,
	"applied"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "django_session" (
	"session_key"	varchar(40) NOT NULL,
	"session_data"	text NOT NULL,
	"expire_date"	datetime NOT NULL,
	PRIMARY KEY("session_key")
);
INSERT INTO "attendance_app_course" VALUES (1,'ijwgr','rg','');
INSERT INTO "attendance_app_emailsettings" VALUES (1,'Your child has arrived at school','Dear parent,

Your child {student_name} has arrived at school at {time_in} on {date}.

Thank you,
School Administration','Your child has left school','Dear parent,

Your child {student_name} has left school at {time_out} on {date}.

Thank you,
School Administration','smtp.gmail.com',587,'','','noreply@school.edu','School Administration');
INSERT INTO "attendance_app_systemsettings" VALUES (1,'Student Monitoring System','CPSC © 2023','','1.0.0');
INSERT INTO "auth_permission" VALUES (1,1,'add_logentry','Can add log entry');
INSERT INTO "auth_permission" VALUES (2,1,'change_logentry','Can change log entry');
INSERT INTO "auth_permission" VALUES (3,1,'delete_logentry','Can delete log entry');
INSERT INTO "auth_permission" VALUES (4,1,'view_logentry','Can view log entry');
INSERT INTO "auth_permission" VALUES (5,2,'add_permission','Can add permission');
INSERT INTO "auth_permission" VALUES (6,2,'change_permission','Can change permission');
INSERT INTO "auth_permission" VALUES (7,2,'delete_permission','Can delete permission');
INSERT INTO "auth_permission" VALUES (8,2,'view_permission','Can view permission');
INSERT INTO "auth_permission" VALUES (9,3,'add_group','Can add group');
INSERT INTO "auth_permission" VALUES (10,3,'change_group','Can change group');
INSERT INTO "auth_permission" VALUES (11,3,'delete_group','Can delete group');
INSERT INTO "auth_permission" VALUES (12,3,'view_group','Can view group');
INSERT INTO "auth_permission" VALUES (13,4,'add_user','Can add user');
INSERT INTO "auth_permission" VALUES (14,4,'change_user','Can change user');
INSERT INTO "auth_permission" VALUES (15,4,'delete_user','Can delete user');
INSERT INTO "auth_permission" VALUES (16,4,'view_user','Can view user');
INSERT INTO "auth_permission" VALUES (17,5,'add_contenttype','Can add content type');
INSERT INTO "auth_permission" VALUES (18,5,'change_contenttype','Can change content type');
INSERT INTO "auth_permission" VALUES (19,5,'delete_contenttype','Can delete content type');
INSERT INTO "auth_permission" VALUES (20,5,'view_contenttype','Can view content type');
INSERT INTO "auth_permission" VALUES (21,6,'add_session','Can add session');
INSERT INTO "auth_permission" VALUES (22,6,'change_session','Can change session');
INSERT INTO "auth_permission" VALUES (23,6,'delete_session','Can delete session');
INSERT INTO "auth_permission" VALUES (24,6,'view_session','Can view session');
INSERT INTO "auth_permission" VALUES (25,7,'add_emailsettings','Can add email settings');
INSERT INTO "auth_permission" VALUES (26,7,'change_emailsettings','Can change email settings');
INSERT INTO "auth_permission" VALUES (27,7,'delete_emailsettings','Can delete email settings');
INSERT INTO "auth_permission" VALUES (28,7,'view_emailsettings','Can view email settings');
INSERT INTO "auth_permission" VALUES (29,8,'add_systemlog','Can add system log');
INSERT INTO "auth_permission" VALUES (30,8,'change_systemlog','Can change system log');
INSERT INTO "auth_permission" VALUES (31,8,'delete_systemlog','Can delete system log');
INSERT INTO "auth_permission" VALUES (32,8,'view_systemlog','Can view system log');
INSERT INTO "auth_permission" VALUES (33,9,'add_systemsettings','Can add system settings');
INSERT INTO "auth_permission" VALUES (34,9,'change_systemsettings','Can change system settings');
INSERT INTO "auth_permission" VALUES (35,9,'delete_systemsettings','Can delete system settings');
INSERT INTO "auth_permission" VALUES (36,9,'view_systemsettings','Can view system settings');
INSERT INTO "auth_permission" VALUES (37,10,'add_section','Can add section');
INSERT INTO "auth_permission" VALUES (38,10,'change_section','Can change section');
INSERT INTO "auth_permission" VALUES (39,10,'delete_section','Can delete section');
INSERT INTO "auth_permission" VALUES (40,10,'view_section','Can view section');
INSERT INTO "auth_permission" VALUES (41,11,'add_course','Can add course');
INSERT INTO "auth_permission" VALUES (42,11,'change_course','Can change course');
INSERT INTO "auth_permission" VALUES (43,11,'delete_course','Can delete course');
INSERT INTO "auth_permission" VALUES (44,11,'view_course','Can view course');
INSERT INTO "auth_permission" VALUES (45,12,'add_attendancerecord','Can add attendance record');
INSERT INTO "auth_permission" VALUES (46,12,'change_attendancerecord','Can change attendance record');
INSERT INTO "auth_permission" VALUES (47,12,'delete_attendancerecord','Can delete attendance record');
INSERT INTO "auth_permission" VALUES (48,12,'view_attendancerecord','Can view attendance record');
INSERT INTO "auth_permission" VALUES (49,13,'add_student','Can add student');
INSERT INTO "auth_permission" VALUES (50,13,'change_student','Can change student');
INSERT INTO "auth_permission" VALUES (51,13,'delete_student','Can delete student');
INSERT INTO "auth_permission" VALUES (52,13,'view_student','Can view student');
INSERT INTO "auth_user" VALUES (1,'pbkdf2_sha256$600000$gpWLBr8rqLzvxwdLf2Yjjn$a8raUhYpcn2WgfjcjzC+pqNNJcNRSjH71PYHxVrlwgY=','2025-06-13 00:02:34.098424',1,'admin','','admin@gmail.com',1,1,'2025-06-12 07:16:41.451305','');
INSERT INTO "auth_user" VALUES (2,'pbkdf2_sha256$600000$jaOHSVGEyhkUFpgLbTvGq8$ATN6bs2vNDOCrXzfOjndLhJXa7DTrFK1qCzjHn5rPro=','2025-06-12 12:51:13.830904',0,'chardoxx','Miculob','miculobrichardvictor@gmail.com',0,1,'2025-06-12 11:51:48.725549','Richard');
INSERT INTO "django_content_type" VALUES (1,'admin','logentry');
INSERT INTO "django_content_type" VALUES (2,'auth','permission');
INSERT INTO "django_content_type" VALUES (3,'auth','group');
INSERT INTO "django_content_type" VALUES (4,'auth','user');
INSERT INTO "django_content_type" VALUES (5,'contenttypes','contenttype');
INSERT INTO "django_content_type" VALUES (6,'sessions','session');
INSERT INTO "django_content_type" VALUES (7,'attendance_app','emailsettings');
INSERT INTO "django_content_type" VALUES (8,'attendance_app','systemlog');
INSERT INTO "django_content_type" VALUES (9,'attendance_app','systemsettings');
INSERT INTO "django_content_type" VALUES (10,'attendance_app','section');
INSERT INTO "django_content_type" VALUES (11,'attendance_app','course');
INSERT INTO "django_content_type" VALUES (12,'attendance_app','attendancerecord');
INSERT INTO "django_content_type" VALUES (13,'attendance_app','student');
INSERT INTO "django_migrations" VALUES (1,'contenttypes','0001_initial','2025-06-12 07:15:59.261482');
INSERT INTO "django_migrations" VALUES (2,'auth','0001_initial','2025-06-12 07:15:59.278553');
INSERT INTO "django_migrations" VALUES (3,'admin','0001_initial','2025-06-12 07:15:59.292997');
INSERT INTO "django_migrations" VALUES (4,'admin','0002_logentry_remove_auto_add','2025-06-12 07:15:59.307107');
INSERT INTO "django_migrations" VALUES (5,'admin','0003_logentry_add_action_flag_choices','2025-06-12 07:15:59.314115');
INSERT INTO "django_migrations" VALUES (6,'contenttypes','0002_remove_content_type_name','2025-06-12 07:15:59.331431');
INSERT INTO "django_migrations" VALUES (7,'auth','0002_alter_permission_name_max_length','2025-06-12 07:15:59.343434');
INSERT INTO "django_migrations" VALUES (8,'auth','0003_alter_user_email_max_length','2025-06-12 07:15:59.355720');
INSERT INTO "django_migrations" VALUES (9,'auth','0004_alter_user_username_opts','2025-06-12 07:15:59.363081');
INSERT INTO "django_migrations" VALUES (10,'auth','0005_alter_user_last_login_null','2025-06-12 07:15:59.374198');
INSERT INTO "django_migrations" VALUES (11,'auth','0006_require_contenttypes_0002','2025-06-12 07:15:59.376178');
INSERT INTO "django_migrations" VALUES (12,'auth','0007_alter_validators_add_error_messages','2025-06-12 07:15:59.384572');
INSERT INTO "django_migrations" VALUES (13,'auth','0008_alter_user_username_max_length','2025-06-12 07:15:59.395638');
INSERT INTO "django_migrations" VALUES (14,'auth','0009_alter_user_last_name_max_length','2025-06-12 07:15:59.405652');
INSERT INTO "django_migrations" VALUES (15,'auth','0010_alter_group_name_max_length','2025-06-12 07:15:59.415639');
INSERT INTO "django_migrations" VALUES (16,'auth','0011_update_proxy_permissions','2025-06-12 07:15:59.421649');
INSERT INTO "django_migrations" VALUES (17,'auth','0012_alter_user_first_name_max_length','2025-06-12 07:15:59.432637');
INSERT INTO "django_migrations" VALUES (18,'sessions','0001_initial','2025-06-12 07:15:59.438636');
INSERT INTO "django_migrations" VALUES (19,'attendance_app','0001_initial','2025-06-12 07:33:21.197502');
INSERT INTO "django_session" VALUES ('17d47m0zg8evy43wd47b35i7yq0uemzb','.eJxVjEEOwiAQRe_C2pBCWxi6dO8ZyEwZLWrAQJtojHe3TbrQ7X_vv7fwuMyTXyoXH4MYhBKH341wvHHaQLhiumQ55jSXSHJT5E6rPOXA9-Pu_gUmrNP6tr0yDYID6FtjNJLtFMFoNCApUHi2weqwEmgUKdTswDl0xD135LDdopVrjTl5fj5ieYmh-XwBTQY-YA:1uPcHq:Ig7zgwDFfHO72ssFyd0gFXlvtVc8wTQFJ8kVLRbAdwA','2025-06-26 07:23:46.404271');
INSERT INTO "django_session" VALUES ('8um5m38bvii0tfxfcegiroc8he0s952u','.eJxVjEEOwiAQRe_C2pBCWxi6dO8ZyEwZLWrAQJtojHe3TbrQ7X_vv7fwuMyTXyoXH4MYhBKH341wvHHaQLhiumQ55jSXSHJT5E6rPOXA9-Pu_gUmrNP6tr0yDYID6FtjNJLtFMFoNCApUHi2weqwEmgUKdTswDl0xD135LDdopVrjTl5fj5ieYmh-XwBTQY-YA:1uPcIp:0O1hh9HVqAVKFvSJhucgLij3Da4dxOjjg4lD4CzVLds','2025-06-26 07:24:47.421407');
INSERT INTO "django_session" VALUES ('v91r2fzbvexo5ftkfx6r232rzm7kpsjp','.eJxVjEEOwiAQRe_C2pBCWxi6dO8ZyEwZLWrAQJtojHe3TbrQ7X_vv7fwuMyTXyoXH4MYhBKH341wvHHaQLhiumQ55jSXSHJT5E6rPOXA9-Pu_gUmrNP6tr0yDYID6FtjNJLtFMFoNCApUHi2weqwEmgUKdTswDl0xD135LDdopVrjTl5fj5ieYmh-XwBTQY-YA:1uPcYS:--lYPO8eVzZ7QAPXr-eEAZxvhBh45h9gj-Dtb6NYHSY','2025-06-26 07:40:56.012464');
INSERT INTO "django_session" VALUES ('xwyj7stuk64yktoui7fpcjt0fxvkhko1','.eJxVjEEOwiAQRe_C2pBCWxi6dO8ZyEwZLWrAQJtojHe3TbrQ7X_vv7fwuMyTXyoXH4MYhBKH341wvHHaQLhiumQ55jSXSHJT5E6rPOXA9-Pu_gUmrNP6tr0yDYID6FtjNJLtFMFoNCApUHi2weqwEmgUKdTswDl0xD135LDdopVrjTl5fj5ieYmh-XwBTQY-YA:1uPcfX:sHzA89MefwAG_CtBaXFicS0gnwK-Q43RMWWOls8njnI','2025-06-26 07:48:15.343896');
INSERT INTO "django_session" VALUES ('uxjxhdxs5c7hk76ppgqyq6scm9b692vw','.eJxVjEEOwiAQRe_C2pBCWxi6dO8ZyEwZLWrAQJtojHe3TbrQ7X_vv7fwuMyTXyoXH4MYhBKH341wvHHaQLhiumQ55jSXSHJT5E6rPOXA9-Pu_gUmrNP6tr0yDYID6FtjNJLtFMFoNCApUHi2weqwEmgUKdTswDl0xD135LDdopVrjTl5fj5ieYmh-XwBTQY-YA:1uPchS:xVr05UdRc3Zeec9Jb-QrZBoklZngz6iKhog4bbljrWQ','2025-06-26 07:50:14.530254');
INSERT INTO "django_session" VALUES ('5a6b8qiireuj9ae8mwf4j82yxiy9intc','.eJxVjEEOwiAQRe_C2pBCWxi6dO8ZyEwZLWrAQJtojHe3TbrQ7X_vv7fwuMyTXyoXH4MYhBKH341wvHHaQLhiumQ55jSXSHJT5E6rPOXA9-Pu_gUmrNP6tr0yDYID6FtjNJLtFMFoNCApUHi2weqwEmgUKdTswDl0xD135LDdopVrjTl5fj5ieYmh-XwBTQY-YA:1uPcya:pCRILsf13xgNQscYAejA3_hWmimUlN97yomms1yxIZw','2025-06-26 08:07:56.875637');
INSERT INTO "django_session" VALUES ('n97h1wqjh6kn3ggise4zcbzgu5ua652g','.eJxVjEEOwiAQRe_C2pBCWxi6dO8ZyEwZLWrAQJtojHe3TbrQ7X_vv7fwuMyTXyoXH4MYhBKH341wvHHaQLhiumQ55jSXSHJT5E6rPOXA9-Pu_gUmrNP6tr0yDYID6FtjNJLtFMFoNCApUHi2weqwEmgUKdTswDl0xD135LDdopVrjTl5fj5ieYmh-XwBTQY-YA:1uPfzw:1APNR2jJ20N2T67GorAGVX_nPPe9DKgSxr_hYJ5DqtY','2025-06-26 11:21:32.266553');
INSERT INTO "django_session" VALUES ('txg7ammto6c8frumlx4sr8oemrdwzbur','.eJxVjEEOwiAQRe_C2pBCWxi6dO8ZyEwZLWrAQJtojHe3TbrQ7X_vv7fwuMyTXyoXH4MYhBKH341wvHHaQLhiumQ55jSXSHJT5E6rPOXA9-Pu_gUmrNP6tr0yDYID6FtjNJLtFMFoNCApUHi2weqwEmgUKdTswDl0xD135LDdopVrjTl5fj5ieYmh-XwBTQY-YA:1uPg2y:Q26ZUBFt0RytqORjvvWE9ETw6v9Q5swr1IG8XU8u1sM','2025-06-26 11:24:40.984668');
INSERT INTO "django_session" VALUES ('2xc6u3pibspwz394npgxjywo9ooy8l85','.eJxVjMEOwiAQRP-FsyErWrb06N1vIAssFjVgoE00xn83JD3oZQ4zb95bWFqX2a6Nq01BTEKJ3W_nyN849yFcKV-K9CUvNTnZEbmtTZ5L4PtpY_8EM7W5v0dWHo5gUANqz-gGDdpFQKXHyPse2gwBzeD1wTsiZ8IYISIpDAa6tHFrqWTLz0eqLzHB5wuBrz8v:1uPgTQ:LdDIV3h7C1Ld5P5XKrWl2qFtObpOT47w-ijbdY9SrGI','2025-06-26 11:52:00.487834');
INSERT INTO "django_session" VALUES ('057dcychsmhj7hfwd18cap3puum3tkz8','.eJxVjEEOwiAQRe_C2pBCWxi6dO8ZyEwZLWrAQJtojHe3TbrQ7X_vv7fwuMyTXyoXH4MYhBKH341wvHHaQLhiumQ55jSXSHJT5E6rPOXA9-Pu_gUmrNP6tr0yDYID6FtjNJLtFMFoNCApUHi2weqwEmgUKdTswDl0xD135LDdopVrjTl5fj5ieYmh-XwBTQY-YA:1uPgqG:4ta7nKV6-ON-43sy9MK_bJlQZDugtSl3x628Knm6-cs','2025-06-26 12:15:36.756102');
INSERT INTO "django_session" VALUES ('ilxgirz711t6pl0tyj9v1t3kz9mhjz5k','.eJxVjMEOwiAQRP-FsyErWrb06N1vIAssFjVgoE00xn83JD3oZQ4zb95bWFqX2a6Nq01BTEKJ3W_nyN849yFcKV-K9CUvNTnZEbmtTZ5L4PtpY_8EM7W5v0dWHo5gUANqz-gGDdpFQKXHyPse2gwBzeD1wTsiZ8IYISIpDAa6tHFrqWTLz0eqLzHB5wuBrz8v:1uPhOj:2jjJ6-fafHC5u4Ffor3Qzpi_zWszG2A9RDqCGnesVTU','2025-06-26 12:51:13.878310');
INSERT INTO "django_session" VALUES ('myt8db4ta9xxjojr4ic9eys1ruk1i2xv','.eJxVjEEOwiAQRe_C2pBCWxi6dO8ZyEwZLWrAQJtojHe3TbrQ7X_vv7fwuMyTXyoXH4MYhBKH341wvHHaQLhiumQ55jSXSHJT5E6rPOXA9-Pu_gUmrNP6tr0yDYID6FtjNJLtFMFoNCApUHi2weqwEmgUKdTswDl0xD135LDdopVrjTl5fj5ieYmh-XwBTQY-YA:1uPrsQ:_le-hVNMiM6NlhC6DSV2AheNImby6CF3XWjwQB4qrh4','2025-06-27 00:02:34.193172');
CREATE INDEX IF NOT EXISTS "attendance_app_attendancerecord_student_id_4497dd97" ON "attendance_app_attendancerecord" (
	"student_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "attendance_app_attendancerecord_student_id_date_d69a4a85_uniq" ON "attendance_app_attendancerecord" (
	"student_id",
	"date"
);
CREATE INDEX IF NOT EXISTS "attendance_app_section_course_id_7a0bafd7" ON "attendance_app_section" (
	"course_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "attendance_app_section_name_course_id_year_level_a84f10ab_uniq" ON "attendance_app_section" (
	"name",
	"course_id",
	"year_level"
);
CREATE INDEX IF NOT EXISTS "attendance_app_student_section_id_67169396" ON "attendance_app_student" (
	"section_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" (
	"group_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" (
	"group_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_permission_content_type_id_2f476e4b" ON "auth_permission" (
	"content_type_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" (
	"content_type_id",
	"codename"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_group_id_97559544" ON "auth_user_groups" (
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_user_id_6a12ed8b" ON "auth_user_groups" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_groups_user_id_group_id_94350c0c_uniq" ON "auth_user_groups" (
	"user_id",
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" (
	"user_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_user_id_c564eba6" ON "django_admin_log" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" (
	"app_label",
	"model"
);
CREATE INDEX IF NOT EXISTS "django_session_expire_date_a5c62663" ON "django_session" (
	"expire_date"
);
COMMIT;
