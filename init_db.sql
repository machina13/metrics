CREATE TABLE "rperf"(
	    "id_server" SMALLINT NOT NULL,
	    "st" BIGINT NOT NULL,
	    "smt2" BIGINT NOT NULL,
	    "smt4" BIGINT NOT NULL,
	    "smt8" BIGINT NOT NULL
);
ALTER TABLE
    "rperf" ADD PRIMARY KEY("id_server");
CREATE TABLE "saps"(
	    "id_server" SMALLINT NOT NULL,
	    "saps_base" BIGINT NOT NULL,
	    "saps_peaks" BIGINT NOT NULL
);
ALTER TABLE
    "saps" ADD PRIMARY KEY("id_server");
CREATE TABLE "spec"(
	    "id_serverbigint" SMALLINT NOT NULL,
	    "base" BIGINT NOT NULL,
	    "peak" BIGINT NOT NULL
);
ALTER TABLE
    "spec" ADD PRIMARY KEY("id_serverbigint");
CREATE TABLE "server"(
	    "bigintid_server" SMALLINT NOT NULL,
	    "name" VARCHAR(255) NOT NULL,
	    "model" VARCHAR(255) NOT NULL,
	    "type" VARCHAR(255) NOT NULL
);
CREATE INDEX "server_bigintid_server_index" ON
    "server"("bigintid_server");
ALTER TABLE
    "server" ADD PRIMARY KEY("bigintid_server");
ALTER TABLE
    "saps" ADD CONSTRAINT "saps_id_server_foreign" FOREIGN KEY("id_server") REFERENCES "server"("bigintid_server");
ALTER TABLE
    "rperf" ADD CONSTRAINT "rperf_id_server_foreign" FOREIGN KEY("id_server") REFERENCES "server"("bigintid_server");
ALTER TABLE
    "spec" ADD CONSTRAINT "spec_id_serverbigint_foreign" FOREIGN KEY("id_serverbigint") REFERENCES "server"("bigintid_server");
