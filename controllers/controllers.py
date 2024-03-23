from odoo import http
from odoo import models, fields, api
from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome
import werkzeug.utils


class ResPartner(models.Model):
    _inherit = 'res.partner'
    cnic = fields.Char(string='CNIC')
    passport = fields.Char(string='Passport')
    last_name = fields.Char(string='Last Name')
    dob = fields.Date(string='Date of Birth')
    work_status = fields.Char(string='Work Status')
    mother = fields.Char(string='Mother')
    city = fields.Char(string='City')
    connection = fields.Char(string='Connection')
    news_medium = fields.Char(string='News Medium')
    mobile = fields.Char(string='Mobile')
    home_phone = fields.Char(string='Home Phone')
    home_extension = fields.Char(string='Home Extension')


class CustomAuthController(AuthSignupHome):
    _inherit = 'res.users'
    _inherit = ''

    @http.route('/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        name = kw.get('name')
        print(name)
        email = kw.get('email')
        print(email)
        password = kw.get('password')
        data = ({
            'name': name,
            'login': email,
            'password': password,
            'groups_id': [(6, 0, [http.request.env.ref('base.group_portal').id])],
        })
        print(data)
        if request.httprequest.method == "POST":
            user = http.request.env['res.users'].sudo().create(data)
            cnic = kw.get('cnic')
            print("this is CNIC >> ", cnic)
            passport = kw.get('passport')
            print("this is passport >> ", passport)
            last_name = kw.get('last_name')
            print("this is last_name >> ", last_name)
            dob = kw.get('dob')
            print("this is dob >> ", dob)
            work_status = kw.get('work_status')
            print("this is work_status >> ", work_status)
            mother = kw.get('mother')
            print("this is mother >> ", mother)
            city = kw.get('city')
            print("this is city >> ", city)
            connection = kw.get('connection')
            print("this is connection >> ", connection)
            news_medium = kw.get('news_medium')
            print("this is news_medium >> ", news_medium)
            mobile = kw.get('mobile')
            print("this is mobile >> ", mobile)
            home_phone = kw.get('home_phone')
            print("this is home_phone >> ", home_phone)
            home_extension = kw.get('home_extension')
            print("this is mother >> ", home_extension)
            partner_data = {
                'cnic': cnic,
                'passport': passport,
                'last_name': last_name,
                'dob': dob,
                'work_status': work_status,
                'mother': mother,
                'city': city,
                'connection': connection,
                'news_medium': news_medium,
                'mobile': mobile,
                'home_phone': home_phone,
                'home_extension': home_extension,
            }
            request.env['res.partner'].search([("id", "=", user.partner_id.id)])
            user.partner_id.write(partner_data)
            return request.render("trionex_website.user_login")
            # return super().web_auth_signup(**kw)
        else:
            return request.render("trionex_website.user_Signup", {})

    @http.route('/web/login', type='http', auth='public', website=True, sitemap=False)
    def my_login(self, *args, **kw):
        login = kw.get('login')
        print(login)
        password = kw.get('password')
        print(password)
        data = ({
            'login': kw.get('login'),
            'password': kw.get('password'),
            'redirect': '/dashboard'})
        # Override the login method to implement custom logic
        # return super(CustomAuthController, self).web_login(*args, **data)
        response = super(CustomAuthController, self).web_login(*args, **data)
        print(response)
        if request.uid and request.env.user.has_group('base.group_portal'):
            # print(request.uid)
            return request.redirect('/dashboard')
        elif request.uid and not request.env.user.has_group('base.group_portal'):
            return request.redirect('/web')
        else:
            return response

    @http.route('/login', type='http', auth='public', website=True, sitemap=False)
    def my_login(self, *args, **kw):
        print('reach / login')
        return request.render("trionex_website.user_login")

    @http.route('/button-click', type='http', auth='public', website=True)
    def my_button_click(self, **kwargs):
        # Determine which button was clicked
        button_clicked = kwargs.get('button')
        print(button_clicked)
        # Redirect to the appropriate page based on which button was clicked
        # if button_clicked == 'login':
        #     return request.render("trionex_website.user_login")
        # return http.request.redirect("/web/login")
        if button_clicked == 'homepage':
            return request.render("trionex_website.custom_homepage")
        elif button_clicked == 'signup':
            return request.render("trionex_website.user_Signup")
            # return http.request.redirect("/usersignup")
        # elif button_clicked == 'logout':
        #     if request.uid and request.env.user.has_group('base.group_portal'):
        #         request.session.logout()
        #         return request.render("trionex_website.custom_homepage", {
        #             'parent': False,
        #             'url': '/homepage',
        #         })
        #         # print(request.uid)
        #         return request.redirect('/dashboard')
        #     elif request.uid and not request.env.user.has_group('base.group_portal'):
        #         request.session.logout()
        #         return request.render("trionex_website.custom_homepage", {
        #             'parent': False,
        #             'url': '/homepage',
        #         })

        else:
            # Handle any other cases (e.g. invalid button clicks)
            return request.redirect('/home')

    @http.route('/web/session/logout', type='http', auth="none")
    # make route /web to / for redirect the internal user on website home rather than default login..
    def logout(self, redirect='/'):
        request.session.logout(keep_db=True)
        return werkzeug.utils.redirect(redirect, 303)

    # @http.route('/homepage', type='http', auth='user', website=True)
    # def homepage(self):
    #     return request.render("trionex_website.custom_homepage", {
    #         'parent': False,
    #         'url': '/about/',
    #     })

    # @http.route('/about/', type='http', auth='user', website=True)
    # def homepage(self):
    #     return request.render("trionex_website.custom_about", {
    #         'parent': False,
    #         'url': '/about/',
    #     })

    # @http.route('/dashboard', type='http', auth='user', website=True)
    # def dashboard(self, **kw):
    #     uid = request.env.uid
    #     user = http.request.env.user
    #     last_login_time = user.login_date
    #     print(f"this is the last log in, {last_login_time}")
    #     client_ip = http.request.httprequest.environ.get('HTTP_X_REAL_IP', http.request.httprequest.remote_addr)
    #     user = request.env.user
    #     # Retrieve personal information for logged-in user
    #     partner = request.env['res.partner'].search([("id", "=", user.partner_id.id)])
    #     # Pass record to template context
    #     context = {
    #         'personal_info': partner,
    #         'last_login': last_login_time.strftime("%d-%m-%Y %H:%M:%S"),
    #         'ip_address': client_ip
    #
    #     return http.request.render('trionex_website.dashboard', context)

    @http.route('/contact', auth='public', website=True)
    def custom_contact(self, **kw):
        # print("user", request.env.user.partner_id.company_id.name)
        print('reach / contact')
        return request.render("mawa_website.custom_contact")

    @http.route('/about', auth='public', website=True)
    def mawa_about(self, **kw):
        return request.render('mawa_website.mawa_about')

    # @http.route('/services/', auth='public', website=True)
    # def custom_services(self, **kw):
    #     print('reach / services')
    #     return request.render("trionex_website.custom_services")

    # @http.route('/home2/', auth='public', website=True)
    # def custom_temp(self, **kw):
    #     KkWebsiteModel = request.env['kk.website']
    #     cards = KkWebsiteModel.search([])
    #     return request.render("trionex_website.custom_homeeess")
    # @http.route('/home2/', auth='public', website=True)
    # def invoices(self, **kw):
    #     invoices = request.env['account.move'].search([])
    #     return http.request.render('trionex_website.custom_homeeess', {'invoices': invoices})