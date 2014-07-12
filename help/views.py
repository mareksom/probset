from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from utils.messages import error_msg, success_msg

@login_required
def latex(request):
	return render(request, 'help/latex.html', {'tab' : 'latex'})

@login_required
def problems(request):
	return render(request, 'help/problems.html', {'tab' : 'problems'})

@login_required
def difficulty(request):
	return render(request, 'help/difficulty.html', {'tab': 'difficulty'})

@login_required
def help(request):
	return redirect('help-bbcode')

@login_required
def bbcode(request):
	lista = (
		"[b]bold[/b]",
		"[i]italics[/i]",
		"[u]underline[/u]",
		"[s]strike[/s]",
		"[b]bold, [i]italic and bold[/b], italic[/i]",
		"[size 30]Huge[/size]",
		"[color red]Red[/color]",
		"[color #0f0]Green[/color]",
		"[center]Center[/center]",
		"[url=http://ki.staszic.waw.pl]Kółko Informatyczne[/url]",
		'[url="http://ki.staszic.waw.pl"]Kółko Informatyczne[/url]',
		"[url http://ki.staszic.waw.pl]Kółko Informatyczne[/url]",
		"[url]http://ki.staszic.waw.pl[/url]",
		"http://ki.staszic.waw.pl",
		"[quote Jack wrote:]That's my quote![/quote]",
		r"\( \sin^2x + \cos^2x = 7 \)",
		r"[latex] \sum_{i=0}^\infty \frac{1}{n^2} = \frac{\sqrt{\pi}}{7} [/latex]",
		"[code python]\ndef square(x):\n\treturn x**2\n[/code]",
		'[code cpp]\n#include <cstdio>\nint main()\n{\n    printf("Hello world!\\n");\n    return 0;\n}\n[/code]',
		"[code brainfuck]\n,>++++++[<-------->-],[<+>-]<.\n[/code]",
		"[img]http://kurier.staszic.waw.pl/images/logo%20lo.png[/img]",
		"[list]\n[*] One\n[*] Two\n[*] Three\n[/list]",
		"[list=1]\n[*] One\n[*] Two\nwrapped\n[*] Three\n[/list]",
		"[list=a]\n[*] One\n[*] Two\n[*]Three\n[/list]",
		"[list=A]\n[*] One\n[*] Two\n[*]Three\n[/list]",
	)
	return render(request, 'help/bbcode.html', {'bbcode_list' : lista, 'tab': 'bbcode' })
