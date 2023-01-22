# flask_framwork
Проект ивключает:
  - Python3
  - Flask
  - SqlAlhemy
  - wtforms
  
Данный код реализует простое Веб-приложение, включающее:
  -Главную страницу
  -Страницу регистрации пользователей
  
  Структрура приложения:
  -- Главный модуль -- app.py
  -- Модуль __init.py__  в котором реализованы экземпляры класса БД, Миграций, Логирования
  -- Модуль routes.py -- реализует маршрутизирование приложение 
  -- Модуль forms.py -- Представляет формы для библиотеки SQLAlhemy- которые создают связь через ORM (Объектно-ориентированное представление) с БД sqlite, куда заносятся
    все данные о зарегистрированном пользователе
  -- Модуль Migrate -- осуществляет миграции для БД sqlite
    
  
  Страница Логин:
  
  
      if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm(csrf_enabled=False)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильный пользователь или пароль!')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Вход', form=form)
  
  Страница Регистрации:
 Для страницы регистрации использовался template register, включающий имя пользователя, mail, пароль. В можуле routes.py реализована проверка на аутентификацию пользователя,
 если пользователь уже зарегистрирован,его перенаправляют на главную страницу. В случае регистрации нового пользователя, его данные заносят в Базу Данных и перенаправляю на главную страницу.
 Для сохранения пароля пользователя используется hash_password--для безопасного сохранения пароля.
 
     if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Ура, вы зарегистрированы!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)
    
    
