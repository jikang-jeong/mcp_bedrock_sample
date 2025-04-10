-- 데이터베이스 접속 후 실행될 SQL 스크립트

CREATE TABLE class (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

-- 주석 추가
COMMENT ON TABLE class IS '수업 정보를 저장하는 테이블';
COMMENT ON COLUMN class.id IS '클래스 고유 ID';
COMMENT ON COLUMN class.name IS '클래스 이름';

-- 학생 테이블 생성
CREATE TABLE student (
    id SERIAL PRIMARY KEY,
    class_id INTEGER REFERENCES class(id)
);

-- 주석 추가
COMMENT ON TABLE student IS '학생 정보를 저장하는 테이블';
COMMENT ON COLUMN student.id IS '학생 고유 ID';
COMMENT ON COLUMN student.class_id IS '학생이 소속된 클래스 ID (class 테이블 참조)';

-- 샘플 데이터 삽입
INSERT INTO class (name) VALUES
('수학'),
('과학'),
('역사');

INSERT INTO student (name, class_id) VALUES
('김민준', 1),
('이서준', 2),
('박지후', 3),
('최지우', 1),
('정하준', 2),
('유주원', 3),
('김예린', 1),
('장서윤', 2),
('한도윤', 3),
('서윤아', 1),
('오지안', 2),
('윤하린', 3),
('신예준', 1),
('강하윤', 2),
('백수아', 3),
('문준호', 1),
('권시우', 2),
('조다인', 3),
('홍지안', 1),
('임나윤', 2),
('배지후', 3),
('남태윤', 1),
('심지우', 2),
('노현우', 3),
('하예빈', 1),
('양하준', 2),
('천윤서', 3),
('구하민', 1),
('전도현', 2),
('민가은', 3);