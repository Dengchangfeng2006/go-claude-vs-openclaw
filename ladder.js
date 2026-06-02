// ═══════ Ranked Ladder System ═══════
const RANKS = ['30k','29k','28k','27k','26k','25k','24k','23k','22k','21k','20k','19k','18k','17k','16k','15k','14k','13k','12k','11k','10k','9k','8k','7k','6k','5k','4k','3k','2k','1k','1d','2d','3d','4d','5d','6d','7d','8d','9d'];

class RankedLadder {
  constructor() {
    this.key = 'go-ladder-v1';
    this.data = this._load();
  }
  _load() {
    try {
      let d = JSON.parse(localStorage.getItem(this.key));
      return d || { wins: 0, losses: 0, unlockedLevel: 1, currentRank: 29, bestRank: 29, games: [], badges: [] };
    } catch { return { wins: 0, losses: 0, unlockedLevel: 1, currentRank: 29, bestRank: 29, games: [], badges: [] }; }
  }
  _save() { localStorage.setItem(this.key, JSON.stringify(this.data)); }

  recordGame(aiLevel, won) {
    this.data.games.push({ level: aiLevel, won, date: new Date().toISOString() });
    if (won) {
      this.data.wins++;
      if (aiLevel >= this.data.unlockedLevel) this.data.unlockedLevel = Math.min(9, aiLevel + 1);
      // Rank up: each win at current level moves rank up
      this.data.currentRank = Math.max(0, this.data.currentRank - 1);
      if (this.data.currentRank < this.data.bestRank) this.data.bestRank = this.data.currentRank;
      this._checkBadges(aiLevel);
    } else {
      this.data.losses++;
      // Rank decays slightly on loss
      this.data.currentRank = Math.min(38, this.data.currentRank + 1);
    }
    this._save();
    return this.getStatus();
  }

  _checkBadges(level) {
    let badges = this.data.badges;
    if (this.data.wins === 1 && !badges.includes('first_win')) badges.push('first_win');
    if (this.data.wins >= 10 && !badges.includes('10wins')) badges.push('10wins');
    if (level >= 7 && !badges.includes('mcts_beaten')) badges.push('mcts_beaten');
    if (this.data.currentRank <= 28 && !badges.includes('single_digit_kyu')) badges.push('single_digit_kyu');
    if (this.data.currentRank <= 20 && !badges.includes('strong_kyu')) badges.push('strong_kyu');
    if (this.data.currentRank <= 0 && !badges.includes('dan_player')) badges.push('dan_player');
  }

  getStatus() {
    return {
      rank: RANKS[this.data.currentRank] || '30k',
      bestRank: RANKS[this.data.bestRank] || '30k',
      unlockedLevel: this.data.unlockedLevel,
      wins: this.data.wins,
      losses: this.data.losses,
      winRate: this.data.wins + this.data.losses > 0 ? Math.round(this.data.wins / (this.data.wins + this.data.losses) * 100) : 0,
      badges: this.data.badges,
      progressToNext: this.data.currentRank > 0 ? Math.round((1 - (this.data.currentRank - Math.floor(this.data.currentRank))) * 100) : 50
    };
  }

  isLevelLocked(level) { return level > this.data.unlockedLevel; }

  reset() { localStorage.removeItem(this.key); this.data = this._load(); }
}

const ladder = new RankedLadder();

function showRankStatus() {
  let s = ladder.getStatus();
  let d = document.getElementById('ladder-panel');
  if (!d) {
    d = document.createElement('div');
    d.id = 'ladder-panel';
    d.style.cssText = 'margin-top:8px;padding:10px;background:rgba(201,169,110,.08);border:1px solid rgba(201,169,110,.2);border-radius:8px;font-size:12px;text-align:center';
    let r = document.getElementById('scoring-panel');
    if (r) r.after(d); else { let el = document.querySelector('.event-bar'); if (el) el.before(d); }
  }
  let badges = s.badges.length ? s.badges.map(b => '<span style="display:inline-block;margin:2px;padding:2px 6px;background:rgba(76,175,80,.15);border-radius:4px;font-size:10px">'+b.replace(/_/g,' ')+'</span>').join('') : 'No badges yet';
  d.innerHTML = '<div style="font-size:16px;font-weight:700;color:#c9a96e">'+s.rank+'</div>'+
    '<div style="color:var(--dim);font-size:11px">Best: '+s.bestRank+' | Win rate: '+s.winRate+'%</div>'+
    '<div style="margin-top:4px;font-size:11px">W'+s.wins+' L'+s.losses+' | Unlocked: Lv.'+s.unlockedLevel+'</div>'+
    '<div style="margin-top:4px">'+badges+'</div>';
}

function onGameEndWithLadder(playerWon, aiLevel) {
  let s = ladder.recordGame(aiLevel, playerWon);
  showRankStatus();
  // Unlock celebration
  if (s.unlockedLevel > 1 && playerWon) {
    document.getElementById('event-text').textContent += ' | 🎉 Lv.'+s.unlockedLevel+' unlocked! Rank: '+s.rank;
  }
}

function applyLevelLocks() {
  let sel = document.getElementById('diff-black');
  if (!sel) return;
  let unlocked = ladder.getStatus().unlockedLevel;
  for (let i = 0; i < sel.options.length; i++) {
    let lv = parseInt(sel.options[i].value);
    if (ladder.isLevelLocked(lv)) {
      sel.options[i].textContent = sel.options[i].textContent.replace(/^Lv\.[0-9]+/, '🔒 Lv.'+lv);
      sel.options[i].disabled = true;
    } else {
      sel.options[i].disabled = false;
    }
  }
}
