CREATE UNIQUE INDEX m_o_idx ON messages USING btree (created_at DESC);