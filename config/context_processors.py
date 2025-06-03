from django.urls import reverse


def _generate_nav(request, links, right = False):
    menu = f'<ul class="navbar-nav{' me-auto' if right else ''}">'
    for link in links:
        app_name, url_name = link['url_name'].split(':')
        if request.resolver_match.url_name == url_name and app_name in request.resolver_match.app_names:
            menu += f"""
                <li class="nav-item">
                    <a class="nav-link active" href="{reverse(link['url_name'])}">{link['title']}
                        <span class="visually-hidden">(current)</span>
                    </a>
                </li>"""
        else:
            menu += f"""
                <li class="nav-item">
                    <a class="nav-link" href="{reverse(link['url_name'])}">{link['title']}</a>
                </li>
                """
    menu += '</ul>'
    return menu


def navigation(request):
    right_nav = ''
    left_nav = _generate_nav(request, [
        {'url_name': 'fintrack:home', 'title': 'Home'},
        {'url_name': 'fintrack:home', 'title': 'Feature'},
        {'url_name': 'fintrack:transactions', 'title': 'Transactions'},
        {'url_name': 'fintrack:home', 'title': 'Pricing'},
        {'url_name': 'fintrack:home', 'title': 'About'},
    ], True)

    if request.user.is_authenticated:
        right_nav = _generate_nav(request, [
            {'url_name': 'account:logout', 'title': 'Logout'},
            {'url_name': 'account:logout', 'title': 'Profile'},
        ])
    else:
        right_nav = _generate_nav(request, [
            {'url_name': 'account:login', 'title': 'Login'},
        ])

    return {'right_nav': right_nav, 'left_nav': left_nav}
