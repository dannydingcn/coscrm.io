from flask import Flask, request, render_template, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
import os,sqlite3
import pandas as pd
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
app.config['SECRET_KEY'] = 'your-secret-key'

db = SQLAlchemy(app)

class DiaryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, default=datetime.utcnow)
    person = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<DiaryEntry {self.date} - {self.person} in {self.location}>'

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.String(50), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(100), nullable=True)
    birth_date = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    nationality = db.Column(db.String(100), nullable=True)
    ethnicity = db.Column(db.String(100), nullable=True)
    id_number = db.Column(db.Integer, nullable=True)
    marital_status = db.Column(db.String(100), nullable=True)
    religion = db.Column(db.String(100), nullable=True)
    drives_car = db.Column(db.Boolean, nullable=True)
    address = db.Column(db.String(100), nullable=True)
    work_address = db.Column(db.String(100), nullable=True)
    phone_number1 = db.Column(db.Integer, nullable=True)
    phone_number2 = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(100), nullable=True)
    wechat = db.Column(db.String(100), nullable=True)
    qq = db.Column(db.String(100), nullable=True)
    weibo = db.Column(db.String(100), nullable=True)
    douyin = db.Column(db.String(100), nullable=True)
    fax = db.Column(db.String(100), nullable=True)
    education_level = db.Column(db.String(100), nullable=True)
    graduation_college = db.Column(db.String(100), nullable=True)
    major = db.Column(db.String(100), nullable=True)
    degree = db.Column(db.String(100), nullable=True)
    academic_achievements = db.Column(db.String(100), nullable=True)
    language_skills = db.Column(db.String(100), nullable=True)
    workplace = db.Column(db.String(100), nullable=True)
    position = db.Column(db.String(100), nullable=True)
    job_level = db.Column(db.String(100), nullable=True)
    job_function = db.Column(db.String(100), nullable=True)
    work_experience_years = db.Column(db.String(100), nullable=True)
    professional_skills = db.Column(db.String(100), nullable=True)
    work_experience = db.Column(db.String(100), nullable=True)
    training_experience = db.Column(db.String(100), nullable=True)
    decision_style = db.Column(db.String(100), nullable=True)
    career_goal_plan = db.Column(db.String(100), nullable=True)
    software_skills = db.Column(db.String(100), nullable=True)
    income_level = db.Column(db.String(100), nullable=True)
    bank_account_info = db.Column(db.String(100), nullable=True)
    financial_status = db.Column(db.String(100), nullable=True)
    credit_record = db.Column(db.String(100), nullable=True)
    investment = db.Column(db.String(100), nullable=True)
    debt = db.Column(db.String(100), nullable=True)
    height = db.Column(db.String(100), nullable=True)
    weight = db.Column(db.String(100), nullable=True)
    blood_type = db.Column(db.String(100), nullable=True)
    health_status = db.Column(db.String(100), nullable=True)
    medical_history = db.Column(db.String(100), nullable=True)
    drug_allergies = db.Column(db.String(100), nullable=True)
    communication_style = db.Column(db.String(100), nullable=True)
    favorite_sports = db.Column(db.String(100), nullable=True)
    favorite_music = db.Column(db.String(100), nullable=True)
    favorite_movies = db.Column(db.String(100), nullable=True)
    favorite_books = db.Column(db.String(100), nullable=True)
    cultural_stance = db.Column(db.String(100), nullable=True)
    moral_beliefs = db.Column(db.String(100), nullable=True)
    worldview = db.Column(db.String(100), nullable=True)
    travel_experience = db.Column(db.String(100), nullable=True)
    dream_destination = db.Column(db.String(100), nullable=True)
    art_preference = db.Column(db.String(100), nullable=True)
    family_members = db.Column(db.String(100), nullable=True)
    spouse_info = db.Column(db.String(100), nullable=True)
    children_info = db.Column(db.String(100), nullable=True)
    friends_info = db.Column(db.String(100), nullable=True)
    emotional_experience = db.Column(db.String(100), nullable=True)
    social_network = db.Column(db.String(100), nullable=True)
    political_stance = db.Column(db.String(100), nullable=True)
    party_affiliation = db.Column(db.String(100), nullable=True)
    criminal_record = db.Column(db.String(100), nullable=True)
    legal_suits = db.Column(db.String(100), nullable=True)
    living_habits = db.Column(db.String(100), nullable=True)
    daily_routine = db.Column(db.String(100), nullable=True)
    unique_hobbies = db.Column(db.String(100), nullable=True)
    eating_habits = db.Column(db.String(100), nullable=True)
    sleeping_habits = db.Column(db.String(100), nullable=True)
    spending_habits = db.Column(db.String(100), nullable=True)
    personality_traits = db.Column(db.String(100), nullable=True)
    emotional_state = db.Column(db.String(100), nullable=True)
    stress_management = db.Column(db.String(100), nullable=True)
    fears_weaknesses = db.Column(db.String(100), nullable=True)
    influence_range = db.Column(db.String(100), nullable=True)
    shared_milestones = db.Column(db.Text(40000), nullable=True)

    def __repr__(self):
        return f'<Customer {self.name}>'

def allowed_file(filename):  

    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']  

 
def create_tables():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    customers = Customer.query.all()
    return render_template('index.html', customers=customers)

@app.route('/import', methods=['GET', 'POST'])  
def import_customers():  
    if request.method == 'POST':  
        # 检查是否有文件上传  
        if 'file' not in request.files:  
            flash('No file part')  
            return redirect(request.url)  
        file = request.files['file']  
        # 如果用户没有选择文件，浏览器会提交一个空的文件名  
        if file.filename == '':  
            flash('No selected file')  
            return redirect(request.url)  
        # 检查文件是否允许上传  
        if file and allowed_file(file.filename):  
            filename = secure_filename(file.filename)  
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  
  
            # 读取Excel文件  
            df = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], filename), engine='openpyxl')  
  
            # 遍历每一行数据  
            for index, row in df.iterrows():  
                # 假设Excel中的第一列是客户的名字  
                name = row[0]  # 根据实际情况修改列索引  
                # 检查数据库中是否已经存在该名字的客户  
                customer = Customer.query.filter_by(name=name).first()  
                if not customer:  
                    # 如果不存在，则创建新客户（这里只列出了部分字段的赋值，您需要根据实际情况补充）  
                    new_customer = Customer(  
                        rating=rating, name=name,  gender = gender, birth_date = birth_date, 
                        age = age, nationality = nationality, ethnicity = ethnicity, id_number = id_number, 
                        marital_status = marital_status, religion = religion,drives_car = drives_car,
                        address = address, work_address = work_address, 
                        phone_number1 = phone_number1, phone_number2 = phone_number2, email = email, 
                        wechat = wechat, qq = qq, weibo = weibo, douyin = douyin, fax = fax, education_level = education_level, 
                        graduation_college = graduation_college, major = major, degree = degree, academic_achievements = academic_achievements, 
                        language_skills = language_skills, workplace = workplace, position = position, job_level = job_level, 
                        job_function = job_function, work_experience_years = work_experience_years, professional_skills = professional_skills,
                         work_experience = work_experience, training_experience = training_experience, decision_style = decision_style, 
                         career_goal_plan = career_goal_plan, software_skills = software_skills, income_level = income_level, 
                         bank_account_info = bank_account_info, financial_status = financial_status, credit_record = credit_record, 
                         investment = investment, debt = debt, height = height, weight = weight, blood_type = blood_type, 
                         health_status = health_status, medical_history = medical_history, drug_allergies = drug_allergies, 
                         communication_style = communication_style, favorite_sports = favorite_sports, favorite_music = favorite_music, 
                         favorite_movies = favorite_movies, favorite_books = favorite_books, cultural_stance = cultural_stance, 
                         moral_beliefs = moral_beliefs, worldview = worldview, travel_experience = travel_experience, 
                         dream_destination = dream_destination, art_preference = art_preference, family_members = family_members, 
                         spouse_info = spouse_info, children_info = children_info, friends_info = friends_info, 
                         emotional_experience = emotional_experience, social_network = social_network, political_stance = political_stance, 
                         party_affiliation = party_affiliation, criminal_record = criminal_record, legal_suits = legal_suits, 
                         living_habits = living_habits, daily_routine = daily_routine, unique_hobbies = unique_hobbies, 
                         eating_habits = eating_habits, sleeping_habits = sleeping_habits, spending_habits = spending_habits, 
                         personality_traits = personality_traits, emotional_state = emotional_state, stress_management = stress_management, 
                         fears_weaknesses = fears_weaknesses, influence_range = influence_range, shared_milestones = shared_milestones
                                    # marital_status=row[某列索引],  # 根据实际情况添加其他字段的赋值  
                        # ...  
                    )  
                    db.session.add(new_customer)  
            # 提交事务  
            db.session.commit()  
            flash('Customers imported successfully!')  
            # 删除上传的Excel文件（可选）  
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))  
            return redirect(url_for('index'))  
    return render_template('import_customers.html')  # 需要您创建一个import_customers.html模板来提供文件上传界面  


@app.route('/export', methods=['GET'])
def export():
    # 查询数据库中的所有客户数据
    customers = Customer.query.all()
    
    # 将查询结果转换为pandas DataFrame
    data = {
        'ID': [c.id for c in customers],
        '评级': [c.rating for c in customers],
        '姓名': [c.name for c in customers],
        '性别': [c.gender for c in customers],
        '出生日期': [c.birth_date for c in customers],
        '年龄': [c.age for c in customers],
        '国籍': [c.nationality for c in customers],
        '种族': [c.ethnicity for c in customers],
        '身份证号': [c.id_number for c in customers],
        '婚姻状况': [c.marital_status for c in customers],
        '宗教信仰': [c.religion for c in customers],
        '是否喜欢开车': [c.drives_car for c in customers],
        '地址': [c.address for c in customers],
        '工作地址': [c.work_address for c in customers],
        '电话号码1': [c.phone_number1 for c in customers],
        '电话号码2': [c.phone_number2 for c in customers],
        '电子邮箱': [c.email for c in customers],
        '微信': [c.wechat for c in customers],
        'QQ': [c.qq for c in customers],
        '微博': [c.weibo for c in customers],
        '抖音': [c.douyin for c in customers],
        '传真': [c.fax for c in customers],
        '教育程度': [c.education_level for c in customers],
        '毕业院校': [c.graduation_college for c in customers],
        '专业': [c.major for c in customers],
        '学位': [c.degree for c in customers],
        '学术成就': [c.academic_achievements for c in customers],
        '语言能力': [c.language_skills for c in customers],
        '工作地点': [c.workplace for c in customers],
        '职位': [c.position for c in customers],
        '职级': [c.job_level for c in customers],
        '工作职责': [c.job_function for c in customers],
        '工作经验年数': [c.work_experience_years for c in customers],
        '专业技能': [c.professional_skills for c in customers],
        '工作经验': [c.work_experience for c in customers],
        '培训经历': [c.training_experience for c in customers],
        '决策风格': [c.decision_style for c in customers],
        '职业规划目标': [c.career_goal_plan for c in customers],
        '软件技能': [c.software_skills for c in customers],
        '收入水平': [c.income_level for c in customers],
        '银行账户信息': [c.bank_account_info for c in customers],
        '财务状况': [c.financial_status for c in customers],
        '信用记录': [c.credit_record for c in customers],
        '投资': [c.investment for c in customers],
        '债务': [c.debt for c in customers],
        '身高': [c.height for c in customers],
        '体重': [c.weight for c in customers],
        '血型': [c.blood_type for c in customers],
        '健康状况': [c.health_status for c in customers],
        '病史': [c.medical_history for c in customers],
        '药物过敏': [c.drug_allergies for c in customers],
        '沟通风格方式': [c.communication_style for c in customers],
        '喜爱的运动': [c.favorite_sports for c in customers],
        '喜爱的音乐': [c.favorite_music for c in customers],
        '喜爱的电影': [c.favorite_movies for c in customers],
        '喜爱的书籍': [c.favorite_books for c in customers],
        '文化立场': [c.cultural_stance for c in customers],
        '道德观念': [c.moral_beliefs for c in customers],
        '世界观': [c.worldview for c in customers],
        '旅行经历': [c.travel_experience for c in customers],
        '梦想目的地': [c.dream_destination for c in customers],
        '艺术偏好': [c.art_preference for c in customers],
        '家庭成员': [c.family_members for c in customers],
        '配偶信息': [c.spouse_info for c in customers],
        '子女信息': [c.children_info for c in customers],
        '朋友信息': [c.friends_info for c in customers],
        '情感体验': [c.emotional_experience for c in customers],
        '社交网络': [c.social_network for c in customers],
        '政治立场': [c.political_stance for c in customers],
        '党派归属': [c.party_affiliation for c in customers],
        '犯罪记录': [c.criminal_record for c in customers],
        '法律诉讼': [c.legal_suits for c in customers],
        '生活习惯': [c.living_habits for c in customers],
        '日常习惯': [c.daily_routine for c in customers],
        '独特爱好': [c.unique_hobbies for c in customers],
        '饮食习惯': [c.eating_habits for c in customers],
        '睡眠习惯': [c.sleeping_habits for c in customers],
        '消费习惯': [c.spending_habits for c in customers],
        '性格特质': [c.personality_traits for c in customers],
        '情绪状态': [c.emotional_state for c in customers],
        '压力管理': [c.stress_management for c in customers],
        '恐惧与弱点': [c.fears_weaknesses for c in customers],
        '影响范围': [c.influence_range for c in customers],
        '共同里程碑': [c.shared_milestones for c in customers],
    }
    df = pd.DataFrame(data)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    # 将DataFrame导出为Excel文件
    excel_file = pd.ExcelWriter('customers{}.xlsx'.format(timestamp), engine='openpyxl')
    df.to_excel(excel_file, index=False)
    excel_file.close()
    
    # 返回Excel文件
    return send_file('customers{}.xlsx'.format(timestamp), as_attachment=True)

@app.route('/add', methods=['GET', 'POST'])
def add_customer():
    if request.method == 'POST':
        rating = request.form.get('rating')
        name = request.form.get('name')
        gender = request.form.get('gender')
        birth_date = request.form.get('birth_date')
        age = request.form.get('age')
        nationality = request.form.get('nationality')
        ethnicity = request.form.get('ethnicity')
        id_number = request.form.get('id_number')
        marital_status = request.form.get('marital_status')
        religion = request.form.get('religion')
        drives_car = request.form.get('drives_car')
        drives_car = drives_car == 'True'
        address = request.form.get('address')
        work_address = request.form.get('work_address')
        phone_number1 = request.form.get('phone_number1')
        phone_number2 = request.form.get('phone_number2')
        email = request.form.get('email')
        wechat = request.form.get('wechat')
        qq = request.form.get('qq')
        weibo = request.form.get('weibo')
        douyin = request.form.get('douyin')
        fax = request.form.get('fax')
        education_level = request.form.get('education_level')
        graduation_college = request.form.get('graduation_college')
        major = request.form.get('major')
        degree = request.form.get('degree')
        academic_achievements = request.form.get('academic_achievements')
        language_skills = request.form.get('language_skills')
        workplace = request.form.get('workplace')
        position = request.form.get('position')
        job_level = request.form.get('job_level')
        job_function = request.form.get('job_function')
        work_experience_years = request.form.get('work_experience_years')
        professional_skills = request.form.get('professional_skills')
        work_experience = request.form.get('work_experience')
        training_experience = request.form.get('training_experience')
        decision_style = request.form.get('decision_style')
        career_goal_plan = request.form.get('career_goal_plan')
        software_skills = request.form.get('software_skills')
        income_level = request.form.get('income_level')
        bank_account_info = request.form.get('bank_account_info')
        financial_status = request.form.get('financial_status')
        credit_record = request.form.get('credit_record')
        investment = request.form.get('investment')
        debt = request.form.get('debt')
        height = request.form.get('height')
        weight = request.form.get('weight')
        blood_type = request.form.get('blood_type')
        health_status = request.form.get('health_status')
        medical_history = request.form.get('medical_history')
        drug_allergies = request.form.get('drug_allergies')
        communication_style = request.form.get('communication_style')
        favorite_sports = request.form.get('favorite_sports')
        favorite_music = request.form.get('favorite_music')
        favorite_movies = request.form.get('favorite_movies')
        favorite_books = request.form.get('favorite_books')
        cultural_stance = request.form.get('cultural_stance')
        moral_beliefs = request.form.get('moral_beliefs')
        worldview = request.form.get('worldview')
        travel_experience = request.form.get('travel_experience')
        dream_destination = request.form.get('dream_destination')
        art_preference = request.form.get('art_preference')
        family_members = request.form.get('family_members')
        spouse_info = request.form.get('spouse_info')
        children_info = request.form.get('children_info')
        friends_info = request.form.get('friends_info')
        emotional_experience = request.form.get('emotional_experience')
        social_network = request.form.get('social_network')
        political_stance = request.form.get('political_stance')
        party_affiliation = request.form.get('party_affiliation')
        criminal_record = request.form.get('criminal_record')
        legal_suits = request.form.get('legal_suits')
        living_habits = request.form.get('living_habits')
        daily_routine = request.form.get('daily_routine')
        unique_hobbies = request.form.get('unique_hobbies')
        eating_habits = request.form.get('eating_habits')
        sleeping_habits = request.form.get('sleeping_habits')
        spending_habits = request.form.get('spending_habits')
        personality_traits = request.form.get('personality_traits')
        emotional_state = request.form.get('emotional_state')
        stress_management = request.form.get('stress_management')
        fears_weaknesses = request.form.get('fears_weaknesses')
        influence_range = request.form.get('influence_range')
        shared_milestones = request.form.get('shared_milestones')
        new_customer = Customer(rating=rating, name=name,  gender = gender, birth_date = birth_date, 
            age = age, nationality = nationality, ethnicity = ethnicity, id_number = id_number, 
            marital_status = marital_status, religion = religion,drives_car = drives_car,
            address = address, work_address = work_address, 
            phone_number1 = phone_number1, phone_number2 = phone_number2, email = email, 
            wechat = wechat, qq = qq, weibo = weibo, douyin = douyin, fax = fax, education_level = education_level, 
            graduation_college = graduation_college, major = major, degree = degree, academic_achievements = academic_achievements, 
            language_skills = language_skills, workplace = workplace, position = position, job_level = job_level, 
            job_function = job_function, work_experience_years = work_experience_years, professional_skills = professional_skills,
             work_experience = work_experience, training_experience = training_experience, decision_style = decision_style, 
             career_goal_plan = career_goal_plan, software_skills = software_skills, income_level = income_level, 
             bank_account_info = bank_account_info, financial_status = financial_status, credit_record = credit_record, 
             investment = investment, debt = debt, height = height, weight = weight, blood_type = blood_type, 
             health_status = health_status, medical_history = medical_history, drug_allergies = drug_allergies, 
             communication_style = communication_style, favorite_sports = favorite_sports, favorite_music = favorite_music, 
             favorite_movies = favorite_movies, favorite_books = favorite_books, cultural_stance = cultural_stance, 
             moral_beliefs = moral_beliefs, worldview = worldview, travel_experience = travel_experience, 
             dream_destination = dream_destination, art_preference = art_preference, family_members = family_members, 
             spouse_info = spouse_info, children_info = children_info, friends_info = friends_info, 
             emotional_experience = emotional_experience, social_network = social_network, political_stance = political_stance, 
             party_affiliation = party_affiliation, criminal_record = criminal_record, legal_suits = legal_suits, 
             living_habits = living_habits, daily_routine = daily_routine, unique_hobbies = unique_hobbies, 
             eating_habits = eating_habits, sleeping_habits = sleeping_habits, spending_habits = spending_habits, 
             personality_traits = personality_traits, emotional_state = emotional_state, stress_management = stress_management, 
             fears_weaknesses = fears_weaknesses, influence_range = influence_range, shared_milestones = shared_milestones
        )
        db.session.add(new_customer)
        db.session.commit()
        flash('Customer added successfully!')
        return redirect(url_for('index'))
    return render_template('add_customer.html')

@app.route('/query')
def query_customer():
    name = request.args.get('name')
    if name:
        customer = Customer.query.filter_by(name=name).first()
        if customer:
            return render_template('query_result.html', customer=customer)
        else:
            flash('No customer found with that name.')
            return redirect(url_for('index'))
    #return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_customer(id):
    customer = Customer.query.get_or_404(id)
    if request.method == 'POST':
        # 更新客户信息
        customer.rating = request.form.get('rating')
        customer.name = request.form.get('name')
        customer.gender = request.form.get('gender')
        customer.birth_date = request.form.get('birth_date')
        customer.age = request.form.get('age')
        customer.nationality = request.form.get('nationality')
        customer.ethnicity = request.form.get('ethnicity')
        customer.id_number = request.form.get('id_number')
        customer.marital_status = request.form.get('marital_status')
        customer.religion = request.form.get('religion')
        customer.drives_car =request.form.get('drives_car')
        customer.drives_car = customer.drives_car == 'True'
        customer.address = request.form.get('address')
        customer.work_address = request.form.get('work_address')
        customer.phone_number1 = request.form.get('phone_number1')
        customer.phone_number2 = request.form.get('phone_number2')
        customer.email = request.form.get('email')
        customer.wechat = request.form.get('wechat')
        customer.qq = request.form.get('qq')
        customer.weibo = request.form.get('weibo')
        customer.douyin = request.form.get('douyin')
        customer.fax = request.form.get('fax')
        customer.education_level = request.form.get('education_level')
        customer.graduation_college = request.form.get('graduation_college')
        customer.major = request.form.get('major')
        customer.degree = request.form.get('degree')
        customer.academic_achievements = request.form.get('academic_achievements')
        customer.language_skills = request.form.get('language_skills')
        customer.workplace = request.form.get('workplace')
        customer.position = request.form.get('position')
        customer.job_level = request.form.get('job_level')
        customer.job_function = request.form.get('job_function')
        customer.work_experience_years = request.form.get('work_experience_years')
        customer.professional_skills = request.form.get('professional_skills')
        customer.work_experience = request.form.get('work_experience')
        customer.training_experience = request.form.get('training_experience')
        customer.decision_style = request.form.get('decision_style')
        customer.career_goal_plan = request.form.get('career_goal_plan')
        customer.software_skills = request.form.get('software_skills')
        customer.income_level = request.form.get('income_level')
        customer.bank_account_info = request.form.get('bank_account_info')
        customer.financial_status = request.form.get('financial_status')
        customer.credit_record = request.form.get('credit_record')
        customer.investment = request.form.get('investment')
        customer.debt = request.form.get('debt')
        customer.height = request.form.get('height')
        customer.weight = request.form.get('weight')
        customer.blood_type = request.form.get('blood_type')
        customer.health_status = request.form.get('health_status')
        customer.medical_history = request.form.get('medical_history')
        customer.drug_allergies = request.form.get('drug_allergies')
        customer.communication_style = request.form.get('communication_style')
        customer.favorite_sports = request.form.get('favorite_sports')
        customer.favorite_music = request.form.get('favorite_music')
        customer.favorite_movies = request.form.get('favorite_movies')
        customer.favorite_books = request.form.get('favorite_books')
        customer.cultural_stance = request.form.get('cultural_stance')
        customer.moral_beliefs = request.form.get('moral_beliefs')
        customer.worldview = request.form.get('worldview')
        customer.travel_experience = request.form.get('travel_experience')
        customer.dream_destination = request.form.get('dream_destination')
        customer.art_preference = request.form.get('art_preference')
        customer.family_members = request.form.get('family_members')
        customer.spouse_info = request.form.get('spouse_info')
        customer.children_info = request.form.get('children_info')
        customer.friends_info = request.form.get('friends_info')
        customer.emotional_experience = request.form.get('emotional_experience')
        customer.social_network = request.form.get('social_network')
        customer.political_stance = request.form.get('political_stance')
        customer.party_affiliation = request.form.get('party_affiliation')
        customer.criminal_record = request.form.get('criminal_record')
        customer.legal_suits = request.form.get('legal_suits')
        customer.living_habits = request.form.get('living_habits')
        customer.daily_routine = request.form.get('daily_routine')
        customer.unique_hobbies = request.form.get('unique_hobbies')
        customer.eating_habits = request.form.get('eating_habits')
        customer.sleeping_habits = request.form.get('sleeping_habits')
        customer.spending_habits = request.form.get('spending_habits')
        customer.personality_traits = request.form.get('personality_traits')
        customer.emotional_state = request.form.get('emotional_state')
        customer.stress_management = request.form.get('stress_management')
        customer.fears_weaknesses = request.form.get('fears_weaknesses')
        customer.influence_range = request.form.get('influence_range')
        customer.shared_milestones = request.form.get('shared_milestones')
        db.session.commit()
        flash('Customer updated successfully!')
        return redirect(url_for('index'))
    return render_template('edit_customer.html', customer=customer)

@app.route('/diary')
def diary_welcome():
    return render_template('diary_welcome.html')

@app.route('/diary_generate', methods=['GET', 'POST'])
def diary_generate():
    if request.method == 'POST':
        date = request.form.get('date')
        person = request.form.get('person')
        location = request.form.get('location')
        content = request.form.get('content')
        new_entry = DiaryEntry(date=date, person=person, location=location, content=content)
        db.session.add(new_entry)
        db.session.commit()
        flash('Diary entry added successfully!')
        return redirect(url_for('diary_welcome'))
    return render_template('diary_generate.html')

@app.route('/diary_modify/<int:id>', methods=['GET', 'POST'])
def diary_modify(id):
    entry = DiaryEntry.query.get_or_404(id)
    if request.method == 'POST':
        entry.date = request.form.get('date', entry.date)
        entry.person = request.form.get('person', entry.person)
        entry.location = request.form.get('location', entry.location)
        entry.content = request.form.get('content', entry.content)
        db.session.commit()
        flash('Diary entry updated successfully!')
        return redirect(url_for('diary_welcome'))
    return render_template('diary_modify.html', entry=entry)

@app.route('/diary_summary')
def diary_summary():
    entries = DiaryEntry.query.order_by(DiaryEntry.date.desc()).all()
    return render_template('diary_summary.html', entries=entries)


if __name__ == '__main__':
    create_tables()
    app.run(debug=True)