from flask import redirect, url_for
from flask_login import login_required
from ez2erp.core.models import CoreModule, CoreModel
from ez2erp.admin import bp_admin
from ez2erp.admin.models import AdminDashboard
from ez2erp.admin.templating import admin_dashboard, DashboardBox, Page, PageConfig



@bp_admin.route('/')
@login_required
def dashboard():
    from ez2erp.auth.models import User

    if AdminDashboard.__view_url__ == 'bp_admin.no_view_url':
        return redirect(url_for('bp_admin.no_view_url'))
    
    options = {
        'box1': DashboardBox("Total Modules","Installed", 0),
        'box2': DashboardBox("System Models","Total models", 0),
        'box3': DashboardBox("Users","Total users", 0)
    }
    page = Page.dashboard()
    return page.display()
    # return admin_dashboard(AdminDashboard, **options)
