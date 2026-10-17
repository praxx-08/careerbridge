import pytest
import requests
from app import create_app

@pytest.fixture()
def app(tmp_path, monkeypatch):
    monkeypatch.delenv('NVIDIA_API_KEY', raising=False)
    monkeypatch.delenv('NVIDIA_MODEL', raising=False)
    app=create_app({'TESTING':True,'SECRET_KEY':'test-only','DATABASE':str(tmp_path/'test.db')})
    assert app.test_cli_runner().invoke(args=['seed']).exit_code==0
    return app

def send(c,path,data,method='POST'):
    token=c.get('/api/session').json['csrf']
    return c.open('/api'+path,method=method,json=data,headers={'X-CSRF-Token':token})

def login(c,email='student@demo.test'):
    return send(c,'/login',{'email':email,'password':'DemoPass123!'})

def test_search_and_assets(app):
    c=app.test_client()
    for path in ['/','/static/app.js','/static/style.css']: assert c.get(path).status_code==200
    assert len(c.get('/api/jobs').json['jobs'])==6
    jobs=c.get('/api/jobs?q=Python&location=Remote&kind=Internship').json['jobs']
    assert len(jobs)==1 and jobs[0]['title']=='Python Developer Intern'
    assert c.get('/api/jobs/9999').status_code==404

def test_registration(app):
    c=app.test_client()
    assert send(c,'/register',{}).status_code==400
    data={'name':'New Student','email':'new@example.test','password':'DemoPass123!','role':'student'}
    assert send(c,'/register',data).status_code==201
    assert send(c,'/register',data).status_code==409
    assert send(c,'/login',{'email':data['email'],'password':'wrong'}).status_code==401
    assert login(c,data['email']).status_code==200
    assert 'password_hash' not in c.get('/api/session').json['user']

def test_csrf_roles_logout(app):
    c=app.test_client()
    assert c.post('/api/login',json={}).status_code==403
    assert c.get('/api/dashboard').status_code==401
    assert login(c).status_code==200
    assert send(c,'/jobs',{}).status_code==403
    assert send(c,'/logout',{}).status_code==200
    assert c.get('/api/dashboard').status_code==401

def test_application_lifecycle(app):
    s,r=app.test_client(),app.test_client()
    login(s);login(r,'recruiter@demo.test')
    assert send(s,'/jobs/1/save',{}).json['saved'] is True
    assert len(s.get('/api/dashboard').json['saved'])==1
    assert send(s,'/jobs/1/save',{}).json['saved'] is False
    payload={'resume':'Python developer with SQL skills and two college projects.','cover_letter':'I would like to contribute my skills to this team.'}
    assert send(s,'/jobs/1/apply',payload).status_code==201
    assert send(s,'/jobs/1/apply',payload).status_code==409
    a=r.get('/api/dashboard').json['applications'][0]
    assert send(r,f"/applications/{a['id']}",{'status':'Interview'},'PATCH').status_code==200
    assert s.get('/api/dashboard').json['applications'][0]['status']=='Interview'
    assert send(r,'/jobs/1',{'status':'closed'},'PATCH').status_code==200
    assert send(s,'/jobs/1/apply',payload).status_code==404

def test_recruiter_ownership_and_publish(app):
    c=app.test_client()
    send(c,'/register',{'name':'Other Recruiter','email':'other@example.test','password':'DemoPass123!','role':'recruiter'})
    login(c,'other@example.test')
    assert send(c,'/jobs/1',{'status':'closed'},'PATCH').status_code==404
    assert send(c,'/applications/1',{'status':'Selected'},'PATCH').status_code==404
    p={'title':'Junior Tester','company':'Test Co','location':'Remote','kind':'Full-time','salary':'₹4 LPA','skills':'Testing','description':'Test web applications and report defects.'}
    result=send(c,'/jobs',p)
    assert result.status_code==201
    assert c.get('/api/jobs/'+str(result.json['id'])).json['job']['title']=='Junior Tester'
    assert len(c.get('/api/dashboard').json['jobs'])==1

def test_coach(app,monkeypatch):
    c=app.test_client();login(c)
    assert send(c,'/coach',{'mode':'review','text':' '}).status_code==400
    payload={'mode':'review','text':'Python developer with portfolio projects'}
    result=send(c,'/coach',payload)
    assert result.status_code==200 and result.json['mode'].startswith('Offline')
    monkeypatch.setenv('NVIDIA_API_KEY','test-key');monkeypatch.setenv('NVIDIA_MODEL','test-model')
    def fail(*args,**kwargs): raise requests.Timeout()
    monkeypatch.setattr('app.requests.post',fail)
    assert send(c,'/coach',payload).status_code==503

def test_persistence_and_seed(app):
    assert app.test_cli_runner().invoke(args=['seed']).exit_code==0
    assert len(app.test_client().get('/api/jobs').json['jobs'])==6
    other=create_app({'TESTING':True,'SECRET_KEY':'test-only','DATABASE':app.config['DATABASE']})
    assert len(other.test_client().get('/api/jobs').json['jobs'])==6
