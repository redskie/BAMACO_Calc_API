import React from 'react';

import {EMPTY_JUDGEMENT_OBJ} from '../constants';
import {calculateScoreInfo} from '../scoreCalc';
import {
  BreakScoreMap,
  FullNoteType,
  Judgement,
  NoteType,
  ScorePerType,
  StrictJudgement,
} from '../types';
import {ScorePage} from './ScorePage';

function calculateJudgementDisplayMap(
  noteJudgements: Map<NoteType, Record<StrictJudgement, number>>
): Map<FullNoteType, Record<Judgement, number>> {
  const res: Map<FullNoteType, Record<Judgement, number>> = new Map();
  const totalCount = {...EMPTY_JUDGEMENT_OBJ};
  noteJudgements.forEach((noteJ, noteType) => {
    res.set(noteType, {
      perfect: noteJ.cp + noteJ.perfect,
      great: noteJ.great,
      good: noteJ.good,
      miss: noteJ.miss,
    });
    // Update total judgement count
    Object.keys(noteJ).forEach((rawJ) => {
      const j = rawJ as StrictJudgement;
      totalCount[j === 'cp' ? 'perfect' : j] += noteJ[j];
    });
  });
  res.set('total', totalCount);
  return res;
}

function calculateApFcStatus(
  totalJudgements: Record<Judgement, number>,
  finaleBorder: Map<string, number>
) {
  if (totalJudgements.miss) {
    return null;
  } else if (finaleBorder.get('AP+') === 0) {
    return 'AP+';
  } else if (totalJudgements.good) {
    return 'FC';
  } else if (totalJudgements.great) {
    return 'FC+';
  }
  return 'AP';
}

interface Props {
  songTitle: string;
  songImgSrc?: string;
  achievement: number;
  noteJudgements: Map<NoteType, Record<StrictJudgement, number>>;
  difficulty?: string;
  track: string;
  date: string;
  place: string;
  highScore?: boolean;
  combo?: string;
  syncStatus?: string;
  rankImg: Map<string, string>;
  apFcImg?: string;
  syncImg?: string;
  fetchRankImage: (title: string) => void;
}
interface State {
  finaleAchievement: number;
  maxFinaleScore: number;
  breakDistribution: BreakScoreMap;
  finaleBorder: Map<string, number>;
  pctPerNoteType: Map<string, number>;
  playerScorePerType: ScorePerType;
  dxAchvPerType: ScorePerType;
  judgementDisplayMap: Map<FullNoteType, Record<Judgement, number>>;
  apFcStatus: string | null;
  achvLossDetail: {
    dx: Map<FullNoteType, Record<Judgement | 'total', number>>;
    finale: Map<FullNoteType, Record<Judgement | 'total', number>>;
  };
}
export class ScorePageContainer extends React.PureComponent<Props, State> {
  static getDerivedStateFromProps(nextProps: Props): State {
    const info = calculateScoreInfo(nextProps.noteJudgements, nextProps.achievement);
    const judgementDisplayMap = calculateJudgementDisplayMap(nextProps.noteJudgements);
    const apFcStatus = calculateApFcStatus(judgementDisplayMap.get('total'), info.finaleBorder);
    return {...info, judgementDisplayMap, apFcStatus};
  }

  render() {
    return <ScorePage {...this.props} {...this.state} />;
  }
}
