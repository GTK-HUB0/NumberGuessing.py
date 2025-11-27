_C='36'
_B=True
_A='31'
import os,math,sys,time,shutil
from datetime import datetime
def supports_ansi():
	if os.name=='nt':return'ANSICON'in os.environ or'WT_SESSION'in os.environ or os.getenv('TERM_PROGRAM')=='vscode'
	return _B
ANSI=supports_ansi()
def color(text,code):return f"[{code}m{text}[0m"if ANSI else text
def clear_screen():os.system('cls'if os.name=='nt'else'clear')
def banner():print(color('MADE BY GTK',_C).center(70))
def clear_screen_except_banner():clear_screen();banner()
class Engine:
	def __init__(A,low,high):A.low=low;A.high=high;A.attempts=0;A.last=None;A.undo_stack=[];A.redo_stack=[];A.bias=0;A.dir_memory=[];A.history=[]
	def save_state(A):A.undo_stack.append((A.low,A.high,A.attempts,A.bias,list(A.dir_memory)))
	def load_state(A,state):A.low,A.high,A.attempts,A.bias,A.dir_memory=state
	def undo(A):
		if not A.undo_stack:print(color('Nothing to undo.',_A));return False
		B=A.undo_stack.pop();A.redo_stack.append((A.low,A.high,A.attempts,A.bias,list(A.dir_memory)));A.load_state(B);return _B
	def redo(A):
		if not A.redo_stack:print(color('Nothing to redo.',_A));return False
		B=A.redo_stack.pop();A.undo_stack.append((A.low,A.high,A.attempts,A.bias,list(A.dir_memory)));A.load_state(B);return _B
	def guess(A):
		C=(A.low+A.high)//2;D=A.bias%3-1;B=C+D
		if len(A.dir_memory)>4:E=sum(A.dir_memory[-4:]);B+=max(-1,min(1,E))
		B=max(A.low,min(A.high,B));A.last=B;return B
	def feed(A,guess,fb):
		B=guess;A.save_state();A.history.append((B,fb,datetime.now()))
		if fb=='h':A.low=B+1;A.dir_memory.append(1);A.bias+=1
		elif fb=='l':A.high=B-1;A.dir_memory.append(-1);A.bias-=1
		A.attempts+=1
	def contradiction(A):return A.low>A.high
def intro():clear_screen();banner();print(color('Commands: H = higher, L = lower, U = undo, R = redo, D = done',_C));input('\nPress Enter to start…')
def prompt_range():
	while _B:
		try:
			A=int(input('Lowest number: '));B=int(input('Highest number: '))
			if B<A:print(color('Highest must be >= lowest.',_A));continue
			return A,B
		except:print(color('Invalid number.',_A))
def show_status(engine):A=engine;print(color(f"Range: {A.low} to {A.high} | Attempts: {A.attempts}",_C));B=A.high-A.low+1;C=math.ceil(math.log2(B))if B>1 else 0;print(color(f"Remaining: {B} | Optimal: {C}",'35'))
def show_history(engine):
	print('\nHistory:')
	for(A,B,C)in engine.history:print(f"{C.strftime("%H:%M:%S")} — {A} → {B.upper()}")
def main():
	D='d';intro();clear_screen_except_banner();print(color('Set your range:',_C));E,F=prompt_range();A=Engine(E,F);clear_screen_except_banner()
	while _B:
		if A.contradiction():print(color('Input contradiction detected.',_A));show_history(A);return
		C=A.guess();print();print(color(f"My guess: {C}",'34'));show_status(A);B=input(color('\n(H/L/U/R/D): ',_C)).strip().lower()
		if B not in('h','l','u','r',D):print(color('Invalid command.',_A));continue
		if B=='u':A.undo();clear_screen_except_banner();continue
		if B=='r':A.redo();clear_screen_except_banner();continue
		if B==D:clear_screen();banner();print(color(f"\nGuessed correctly: {C}",'32'));print(color(f"Attempts: {A.attempts+1}",'32'));A.history.append((C,D,datetime.now()));show_history(A);return
		A.feed(C,B);clear_screen_except_banner()
if __name__=='__main__':
	try:main()
	except KeyboardInterrupt:print('\nExiting.')
