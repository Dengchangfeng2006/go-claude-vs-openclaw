with open('/e/go-claude-vs-openclaw/index.html', 'r') as f:
    html = f.read()

# MCTS module
mcts = """class MCTSNode{constructor(move,parent){this.move=move;this.parent=parent;this.children={};this.visits=0;this.wins=0}
uct(c){if(!this.visits)return Infinity;let total=0;for(let k in this.parent.children)total+=this.parent.children[k].visits;return this.wins/this.visits+c*Math.sqrt(Math.log(total)/this.visits)}}
class MCTSGoAI extends GoAI{
  constructor(color,diff=5,playouts=600){super(color,diff);this.playouts=Math.max(300,Math.min(1000,playouts))}
  selectMove(game){
    let moves=game.getLegalMoves();if(!moves.length)return null;if(moves.length===1)return moves[0];
    let root=new MCTSNode(null,null),deadline=Date.now()+2500;
    for(let m of moves)root.children[m.row+','+m.col]=new MCTSNode(m,root);
    for(let i=0;i<this.playouts&&Date.now()<deadline;i++){
      let state=game.clone(),node=root;
      while(Object.keys(node.children).length>0){let best=null,bu=-Infinity;for(let k in node.children){let u=node.children[k].uct(1.4);if(u>bu){bu=u;best=node.children[k]}}if(!best)break;state.play(best.move.row,best.move.col);node=best}
      let unexpanded=[];for(let k in node.children)if(!node.children[k].visits){unexpanded.push(node.children[k]);break}
      if(unexpanded.length){let child=unexpanded[0];state.play(child.move.row,child.move.col);node=child}
      let sim=state.clone(),steps=0;while(!sim.gameOver&&steps<80){let sm=sim.getLegalMoves();if(!sm.length)break;let m=sm[Math.floor(Math.random()*sm.length)];sim.play(m.row,m.col);steps++}
      let score;if(sim.gameOver){let t=sim.estimateTerritory(),bs=t.black+sim.captures[0],ws=t.white+sim.captures[1]+sim.komi;score=this.playerColor===1?(bs>ws?1:0):(ws>bs?1:0)}else{score=0.5}
      let back=node;while(back){back.visits++;back.wins+=score;back=back.parent}}
    let best=null,bv=-1;for(let k in root.children){let c=root.children[k];if(c.visits>bv){bv=c.visits;best=c.move}}
    return best||super.selectMove(game)}}"""

html = html.replace("class GoAI{", mcts + "class GoAI{")

print("Patch 1: MCTS inserted")

# SGF import
sgf_import = """function parseSGF(sgf){function idx(c){return'abcdefghjklmnopqrst'.indexOf(c)}let d=0,s=-1,e=-1;for(let i=0;i<sgf.length;i++){if(sgf[i]==='('){if(d===0)s=i;d++}else if(sgf[i]===')'){d--;if(d===0){e=i;break}}}let nodes=sgf.slice(s+1,e).split(';').filter(n=>n.trim()),meta={blackName:'',whiteName:'',komi:'',result:'',date:'',size:19},moves=[];for(let node of nodes){let props={},m,re=/([A-Z]+)\\[([^\\]]*)\\]/g;while((m=re.exec(node))!==null)props[m[1]]=m[2];if(props.PB)meta.blackName=props.PB;if(props.PW)meta.whiteName=props.PW;if(props.KM)meta.komi=props.KM;if(props.RE)meta.result=props.RE;if(props.DT)meta.date=props.DT;if(props.SZ)meta.size=+props.SZ;if(props.B!==undefined)moves.push(props.B===''?{row:-1,col:-1,player:1}:{row:idx(props.B[1]),col:idx(props.B[0]),player:1});if(props.W!==undefined)moves.push(props.W===''?{row:-1,col:-1,player:2}:{row:idx(props.W[1]),col:idx(props.W[0]),player:2})}return{moves,metadata:meta}}
function importSGFToGame(game,sgf){let{moves}=parseSGF(sgf);for(let m of moves){if(m.row===-1)game.pass();else game.play(m.row,m.col)}}
function loadSGFFile(){let input=document.createElement('input');input.type='file';input.accept='.sgf';input.onchange=e=>{let file=e.target.files[0],reader=new FileReader();reader.onload=()=>{resetGame();importSGFToGame(game,reader.result);renderer.draw();updateUI();document.getElementById('event-text').textContent='SGF imported'};reader.readAsText(file)};input.click()}"""

html = html.replace("function copySGFToClipboard", sgf_import + "function copySGFToClipboard")

print("Patch 2: SGF import inserted")

# Use MCTS at difficulty >= 7
html = html.replace(
    "aiBlack=new GoAI(1,parseInt(document.getElementById('diff-black').value));aiWhite=new GoAI(2,parseInt(document.getElementById('diff-white').value))",
    "let db=parseInt(document.getElementById('diff-black').value),dw=parseInt(document.getElementById('diff-white').value);aiBlack=db>=7?new MCTSGoAI(1,db,db*100):new GoAI(1,db);aiWhite=dw>=7?new MCTSGoAI(2,dw,dw*100):new GoAI(2,dw)"
)

print("Patch 3: MCTS difficulty wiring")

# End-game + analysis
endgame = """function chineseScore(g){let b=0,w=0;for(let r=0;r<g.size;r++)for(let c=0;c<g.size;c++){if(g.board[r][c]===1)b++;else if(g.board[r][c]===2)w++}let t=g.estimateTerritory();return{black:b+t.black,white:w+t.white+g.komi}}
function japaneseScore(g){let t=g.estimateTerritory();return{black:t.black+g.captures[0],white:t.white+g.captures[1]+g.komi}}
function showScoring(){let cn=chineseScore(game),jp=japaneseScore(game),d=document.getElementById('scoring-panel');if(!d){d=document.createElement('div');d.id='scoring-panel';d.style.cssText='margin-top:12px;padding:12px;background:rgba(255,255,255,.05);border-radius:8px;font-size:12px';document.querySelector('.info-panel').appendChild(d)}let wr=(a,b)=>a>b?'<span style=color:#ff6b6b>Black wins</span>':b>a?'<span style=color:#4ecdc4>White wins</span>':'Draw';d.innerHTML='<div style=display:flex;gap:12px;margin-bottom:8px><div style=flex:1><b>Chinese (area)</b><br>B:'+cn.black.toFixed(1)+' W:'+cn.white.toFixed(1)+'<br>'+wr(cn.black,cn.white)+'</div><div style=flex:1><b>Japanese (territory)</b><br>B:'+jp.black.toFixed(1)+' W:'+jp.white.toFixed(1)+'<br>'+wr(jp.black,jp.white)+'</div></div><div style=display:flex;gap:6px><button onclick=confirmEnd() style=flex:1;padding:6px;border:1px solid #4caf50;border-radius:4px;background:rgba(76,175,80,.15);color:#4caf50;cursor:pointer;font-size:12px>Confirm End</button><button onclick=resumePlay() style=flex:1;padding:6px;border:1px solid #ff6b6b;border-radius:4px;background:rgba(255,107,107,.15);color:#ff6b6b;cursor:pointer;font-size:12px>Resume</button></div>'}
function confirmEnd(){let d=document.getElementById('scoring-panel');if(d)d.remove();game._cp=false;game.gameOver=true;endGame()}
function resumePlay(){let d=document.getElementById('scoring-panel');if(d)d.remove();game._cp=false;game.passes=0;game.gameOver=false;updateUI();renderer.draw();if(!humanMode||game.currentPlayer!==humanColor)scheduleNextMove()}"""
analysis_mod = """function analyzeGame(game){let t=game.estimateTerritory();return{movesTotal:game.moveHistory.length,capturesByBlack:game.captures[0],capturesByWhite:game.captures[1],territoryBlack:t.black,territoryWhite:t.white,openingUsed:game.moveHistory.length>=4?'Star point':'Custom',avgThinkTime:'N/A'}}
function showAnalysis(){let a=analyzeGame(game),d=document.getElementById('analysis-panel');if(!d){d=document.createElement('div');d.id='analysis-panel';d.style.cssText='margin-top:12px;padding:14px;background:rgba(201,169,110,.08);border:1px solid rgba(201,169,110,.3);border-radius:8px;font-size:12px';let r=document.getElementById('scoring-panel');if(r)r.after(d);else document.querySelector('.info-panel').appendChild(d)}d.innerHTML='<h4 style=color:#c9a96e;margin-bottom:8px>Game Analysis</h4><div style=display:grid;grid-template-columns:1fr 1fr;gap:4px>'+[['Moves',a.movesTotal],['B Captures',a.capturesByBlack],['W Captures',a.capturesByWhite],['B Territory',a.territoryBlack],['W Territory',a.territoryWhite],['Opening',a.openingUsed]].map(([k,v])=>'<div>'+k+': <b>'+v+'</b></div>').join('')+'</div>'}"""

html = html.replace("window.addEventListener('resize'", endgame + analysis_mod + "window.addEventListener('resize'")

print("Patch 4: End-game scoring + analysis inserted")

# SGF import button
html = html.replace(
    "</button></div></div>",
    "</button><button class=\"btn-sm\" onclick=\"loadSGFFile()\">Import SGF</button></div></div>"
)

print("Patch 5: Import button added")

# Show scoring + analysis on game end
html = html.replace("et.textContent='", "showAnalysis();showScoring();et.textContent='")

print("Patch 6: Scoring on end")

# MCTS badge
html = html.replace(
    "<span class=\"badge\" id=\"badge-ko\">Ko</span>",
    "<span class=\"badge\" id=\"badge-ko\">Ko</span><span class=\"badge\" id=\"badge-mcts\">MCTS</span>"
)

html = html.replace(
    "document.getElementById('badge-search').className=(game.moveHistory.length>20&&game.getLegalMoves().length<40)?'badge on':'badge'",
    "document.getElementById('badge-search').className=(game.moveHistory.length>20&&game.getLegalMoves().length<40)?'badge on':'badge';document.getElementById('badge-mcts').className=(aiBlack instanceof MCTSGoAI||aiWhite instanceof MCTSGoAI)?'badge on':'badge'"
)

print("Patch 7: MCTS badge")

with open('/e/go-claude-vs-openclaw/index.html', 'w') as f:
    f.write(html)

print(f"Done! {len(html)} bytes")
