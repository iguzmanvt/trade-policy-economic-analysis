"""Build the English note and its figure from the validated P04 result tables.

Optional dependencies: matplotlib and reportlab. Core accounting reproduction
remains standard-library-only in analyze.py. No network access is required.
Edit the prose blocks in this file, then rebuild to keep NOTE.md and NOTE.pdf
consistent. All displayed numerical results are derived from the result CSVs.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import tempfile
from decimal import Decimal as D
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent
NAVY = '#002060'
PALE = '#AFC2DE'
INK = '#202B38'
REVIEW_DATE = '26 October 2026'
TITLE = 'Import exposure depends on the use being measured'


def read_csv(name):
    with (ROOT / 'results' / name).open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def number(value, places=3):
    return f'{D(value):,.{places}f}'


def percent(value):
    return f'{D(value):.1f}%'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_evidence():
    origin = {r['origin']: r for r in read_csv('origin_and_uses.csv')}
    groups = read_csv('intermediate_destination_groups.csv')
    finals = {r['component']: r for r in read_csv('final_uses.csv')}
    universes = {r['table']: r for r in read_csv('universe_comparison.csv')}
    validation = json.loads((ROOT / 'results/validation.json').read_text())
    if validation['input_sha256'] != sha(ROOT / 'data/official_cells.csv'):
        raise ValueError('Publication refused: input differs from the validated snapshot; run analyze.py.')
    if set(origin) != {'D', 'M'} or len(groups) != 6 or set(universes) != {'MIP', 'COU'}:
        raise ValueError('Publication refused: incomplete result-table coverage.')
    inter = sum(D(r['intermediate']) for r in origin.values())
    final = sum(D(r['final']) for r in origin.values())
    gross = sum(D(r['all_uses']) for r in origin.values())
    if inter + final != gross or sum(D(r['total']) for r in groups) != inter:
        raise ValueError('Publication refused: result totals do not reconcile.')
    if sum(D(r['total']) for r in finals.values()) != final:
        raise ValueError('Publication refused: final components do not reconcile.')
    if D(universes['MIP']['gross_all_uses']) != gross:
        raise ValueError('Publication refused: MIP universe denominator differs.')
    if any(D(r['domestic']) + D(r['imported']) != D(r['total']) for r in groups):
        raise ValueError('Publication refused: destination origin totals differ.')
    sources = json.loads((ROOT / 'sources.json').read_text(encoding='utf-8'))
    return origin, groups, finals, universes, validation, inter, final, gross, sources


def make_figure(groups):
    # A temporary font cache also works in read-only home directories.
    if 'MPLCONFIGDIR' not in os.environ:
        cache = Path(tempfile.gettempdir()) / 'p04-matplotlib-cache'
        cache.mkdir(exist_ok=True)
        os.environ['MPLCONFIGDIR'] = str(cache)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter

    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'svg.hashsalt': 'p04-destination-origin-2018',
                         'pdf.fonttype': 42, 'ps.fonttype': 42})
    labels = {
        'Food and beverage services': 'Food and beverage\nservices',
        'Dairy products': 'Dairy products',
        'Other food and beverages': 'Other food and\nbeverages',
        'Other products and services': 'Other products and\nservices',
        'Education, health and government services': 'Education, health and\ngovernment services',
        'Other manufactures': 'Other manufactures',
    }
    fig, ax = plt.subplots(figsize=(9.5, 5.25), facecolor='white')
    fig.subplots_adjust(left=.265, right=.96, bottom=.14, top=.75)
    y = list(range(len(groups)))
    domestic = [float(r['domestic']) for r in groups]
    imported = [float(r['imported']) for r in groups]
    ax.barh(y, domestic, height=.59, color=PALE, label='Domestic origin', linewidth=0)
    ax.barh(y, imported, left=domestic, height=.59, color=NAVY, label='Imported origin', linewidth=0)
    for pos, row in enumerate(groups):
        ax.text(float(row['total']) + 75, pos, number(row['total'], 1),
                va='center', ha='left', color=INK, fontsize=10)
    ax.set_yticks(y, [labels[r['destination_group']] for r in groups])
    ax.invert_yaxis()
    ax.set_xlim(0, 6100)
    ax.set_xticks([0, 1000, 2000, 3000, 4000, 5000, 6000])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:,.0f}'))
    ax.tick_params(axis='y', length=0, pad=10, colors=INK)
    ax.tick_params(axis='x', length=4, color='#657487', labelcolor=INK)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    for side in ('left', 'bottom'):
        ax.spines[side].set_color('#657487')
        ax.spines[side].set_linewidth(.7)
    ax.grid(False)
    fig.suptitle('Intermediate uses by destination product group', x=.52, y=.965,
                 fontsize=15, color=NAVY, weight='bold')
    fig.text(.52, .905, 'MIP 311513 | 2018 | million pesos at basic prices',
             ha='center', fontsize=10, color=INK)
    handles, legend_labels = ax.get_legend_handles_labels()
    fig.legend(handles, legend_labels, loc='upper center', bbox_to_anchor=(.53, .875),
               ncol=2, frameon=False, fontsize=10)
    fig.text(.265, .025, 'Source: INEGI MIP 2018; author grouping. Labels show both-origin totals.',
             ha='left', fontsize=8, color='#536173')
    dest = ROOT / 'figures'
    dest.mkdir(exist_ok=True)
    fig.savefig(dest / 'intermediate_destination_origins.png', dpi=240,
                metadata={'Software': 'P04 build_publication.py'})
    fig.savefig(dest / 'intermediate_destination_origins.svg',
                metadata={'Date': None, 'Creator': 'P04 build_publication.py'})
    plt.close(fig)


def make_blocks(e):
    origin, groups, finals, universes, validation, inter, final, gross, sources = e
    imp = origin['M']
    top_three = sum(D(r['total']) for r in groups[:3]) / inter * 100
    imported_final_share = D(imp['final']) / final * 100
    intermediate_share = inter / gross * 100
    total_import_share = D(imp['all_uses']) / gross * 100
    imported_inter_share = D(imp['intermediate']) / inter * 100
    published_final = final - D(imp['all_uses'])
    source_recovery = sources.get('current_recovery_summary',
        'The archived extract and its historical workbook identities are preserved; '
        'see sources.json for the separately dated source-recovery record.')
    audit_path = ROOT / 'data/source_recovery_20261026.json'
    if audit_path.is_file():
        audit = json.loads(audit_path.read_text(encoding='utf-8'))
        if audit.get('status') == 'EXACT_OFFICIAL_BINARIES_RECOVERED':
            source_recovery = (
                f'All {audit["official_binary_count"]} official workbooks were downloaded again on '
                f'{REVIEW_DATE}; all {audit["binary_hash_matches"]} hashes match the archived files. '
                f'The {audit["selected_cell_values_compared"]:,} selected cells agree, with '
                f'{audit["selected_cell_value_mismatches"]} differences. This checks the selected '
                'extraction, not every account in the full matrices.')
    rows_origin = [
        ['Product origin', 'Intermediate\nuses', 'Final\nuses', 'All gross\nuses', 'Intermediate /\nthat origin'],
        ['Domestic', number(origin['D']['intermediate']), number(origin['D']['final']),
         number(origin['D']['all_uses']), percent(origin['D']['intermediate_share_of_origin_pct'])],
        ['Imported', number(imp['intermediate']), number(imp['final']),
         number(imp['all_uses']), percent(imp['intermediate_share_of_origin_pct'])],
        ['Both origins', number(inter), number(final), number(gross), percent(intermediate_share)],
    ]
    rows_groups = [['Destination product group', 'Share of all\nintermediate uses', 'Imported share of\n311513 uses in group']]
    rows_groups += [[r['destination_group'], percent(r['share_of_intermediate_pct']),
                     percent(r['imported_share_within_group_pct'])] for r in groups[:3]]
    rows_data = [
        ['Economic question', 'Additional evidence required'],
        ['Which flows face the policy?', 'Tariff-line concordance to 311513; affected products, countries of origin of imports, policy provisions and dates.'],
        ['Can users substitute?', 'Product specifications and quantities, domestic and imported prices, supplier switching, contracts, available capacity and substitution elasticities.'],
        ['What are compliance costs?', 'Firm or product evidence on certification, testing, labelling and administration; fixed versus recurring costs and adjustment time.'],
        ['How do prices and output respond?', 'The input share in each user\'s total costs; import, producer and consumer prices; exchange rates, margins, market structure, inventories and compatible output data.'],
    ]
    return [
        ('title', TITLE),
        ('meta', f'Isaac Guzmán Valdivia Tovar | P04 | Reviewed {REVIEW_DATE} | Data: 2018'),
        ('lead', f'Imported origin: {percent(imported_inter_share)} of intermediate uses; '
         f'{percent(total_import_share)} of all gross uses.'),
        ('heading', 'Question and trade-policy relevance'),
        ('p', 'How does imported-origin exposure differ between intermediate and total uses of Mexico\'s '
         'dairy-derivatives category, and which destination product groups account for its intermediate demand?'),
        ('p', f'In the 2018 accounts, the imported-origin share of intermediate uses is '
         f'{percent(imported_inter_share)}, against {percent(total_import_share)} for all gross uses. '
         f'Food and beverage services, dairy products, and other food and beverages account for '
         f'{percent(top_three)} of intermediate demand. These distinctions help identify where to '
         'investigate the consequences of a product-specific trade-policy change. They establish the '
         'allocation of recorded uses; a price or output response requires additional evidence. [1]'),
        ('heading', 'A product row with explicit denominators'),
        ('p', 'The National Institute of Statistics and Geography (INEGI) publishes the 2018 input-output '
         'matrix (MIP, its Spanish acronym). This exercise uses its symmetric, product-by-product table '
         'and the class associated with code 311513 in the North American Industry Classification System, '
         'Mexico 2018 (SCIAN). The official label is “Elaboración de derivados y fermentos lácteos”. '
         'It covers dairy derivatives and fermented dairy products, including cheese and imitation cheese; '
         'it does not isolate cheese names. Rows record products used; intermediate columns represent '
         'homogeneous destination product groups. Values are millions of pesos at basic prices for 2018. [1, 3]'),
        ('table', rows_origin, [83, 94, 94, 98, 106]),
        ('small', 'Table 1. All values except the last column are million pesos. The last column divides '
         'intermediate uses by all uses of the same row. Both origins means domestic plus imported, counted once. '
         'Source: MIP_19 and MIP_38, Tabulado, row 196; author calculations.'),
        ('p', f'The {percent(imported_inter_share)} ratio is {number(imp["intermediate"])} / {number(inter)}: '
         'imported intermediate uses divided by intermediate uses of both origins. The '
         f'{percent(total_import_share)} ratio is {number(imp["all_uses"])} / {number(gross)}: all imported-origin '
         f'uses divided by all gross uses. In contrast, {percent(imp["intermediate_share_of_origin_pct"])} '
         f'is {number(imp["intermediate"])} / {number(imp["all_uses"])}: the share of imported-origin uses '
         'that goes to intermediate demand.'),
        ('p', f'Intermediate uses account for {percent(intermediate_share)} of gross uses, while final '
         f'uses account for {percent(100-intermediate_share)} and have an imported-origin share of '
         f'{percent(imported_final_share)}. This composition explains the lower aggregate import share. '
         '“Gross uses” means uses before the combined table\'s imports-netting adjustment; it includes '
         'exports and signed inventory changes. It is not a measure of imported content in production or foreign value added.'),
        ('page',),
        ('heading', 'Where intermediate demand is concentrated'),
        ('p', f'The snapshot retains all {validation["MIP_product_destinations"]} intermediate destinations '
         f'for each origin, including the {validation["MIP_product_destinations"]-validation["MIP_positive_destinations"]} '
         f'zero-flow destinations in the combined row. The {validation["MIP_positive_destinations"]} positive '
         'destinations are assigned once to six exhaustive analytical groups using SCIAN code prefixes. '
         'The figure separates domestic and imported values within each group. [1]'),
        ('figure', 'figures/intermediate_destination_origins.png'),
        ('small', 'Figure 1. Each bar sums domestic and imported uses of category 311513. '
         'The groups describe destination products, not individual purchasing firms or retail channels. '
         'All six groups and exact values are in results/intermediate_destination_groups.csv.'),
        ('table', rows_groups, [249, 113, 113]),
        ('small', 'Table 2. The first percentage uses all intermediate demand of 311513 as its denominator. '
         'The second uses only the total 311513 flow into that destination group, not all inputs used by the group.'),
        ('p', 'The largest destination and the highest imported share answer different screening questions. '
         f'Food and beverage services has the largest flow, {number(groups[0]["total"])} million pesos, '
         f'with {percent(groups[0]["imported_share_within_group_pct"])} imported origin. Other food and '
         f'beverages has a smaller flow but an imported share of '
         f'{percent(groups[2]["imported_share_within_group_pct"])}. These results identify different '
         'links to examine. Neither ranks vulnerability: a large flow may be readily replaceable, while '
         'a smaller specialised input may face few substitutes.'),
        ('page',),
        ('heading', 'Reconciliation and a separate comparison'),
        ('p', f'Domestic plus imported values equal the combined-origin intermediate row in every '
         f'destination, and destination sums equal {number(inter)} million pesos. Final components '
         f'sum to {number(final)}: private consumption is {number(finals["private_consumption"]["total"])} '
         f'({percent(finals["private_consumption"]["share_of_final_pct"])} of final uses), exports '
         f'{number(finals["exports"]["total"])}, and inventory change '
         f'{number(finals["inventories"]["total"])}. Government consumption, fixed capital and the '
         'statistical discrepancy are zero. The negative inventory value remains in the final-use '
         'and gross-use totals. [1]'),
        ('p', f'MIP_10 includes a negative imports entry in its final-demand block. The bridge is '
         f'**{number(published_final)} - (-{number(imp["all_uses"])}) = {number(final)}** million pesos '
         f'of gross final uses. Adding {number(inter)} of intermediate uses gives '
         f'{number(gross)} of gross uses. This restores the same gross accounting presentation as '
         'the domestic-plus-imported sum; the negative imports entry is not an extra demand flow.'),
        ('p', 'The supply-and-use tables (COU, their Spanish acronym) provide a separate comparison for '
         'the broader SCIAN branch 3115, “Elaboración de productos lácteos”. The row is a product '
         'category; columns identify user industries. Its '
         f'{number(universes["COU"]["intermediate"])} million pesos of intermediate uses divided by '
         f'{number(universes["COU"]["gross_all_uses"])} of total uses gives '
         f'**{percent(universes["COU"]["intermediate_share_pct"])}**. This is the intermediate-use share '
         f'of another category, not another imported-origin proportion. It cannot be treated as a '
         f'revision of MIP 311513\'s {percent(intermediate_share)} share. [2, 3]'),
        ('heading', 'The next economic question'),
        ('p', 'For a specified change in market access, which affected dairy inputs could users replace, '
         'at what cost and over what period? The accounts organise that inquiry, but do not answer it. '
         'A focused follow-up would link the affected products and countries of origin of imports to '
         'the destination groups, then assemble the evidence below.'),
        ('table', rows_data, [121, 354]),
        ('p', 'Updated supply-and-use or transaction evidence would also be needed to assess how far the '
         '2018 structure remains applicable. Estimating indirect production requirements would require '
         'the relevant complete matrix and stated assumptions; identifying a causal policy effect would '
         'require a credible comparison design. The present result closes as a reproducible accounting '
         'decomposition. It identifies no firms, retail channels, named cheeses or bilateral suppliers, '
         'and estimates no substitution, compliance cost, price transmission or production effect.'),
        ('small', f'Source verification. {source_recovery} The original 2018 reference year and '
         '29 August 2023 workbook metadata remain unchanged. See sources.json, data/workbook_provenance.json '
         'and VALIDATION.md for exact identities and execution scope.'),
        ('sources', [
            ('[1] INEGI. MIP 2018, product-by-product, class level. MIP_19, MIP_38 and MIP_10; Tabulado row 196.', 'https://www.inegi.org.mx/programas/mip/2018/'),
            ('[2] INEGI. COU 2018, basic-price use, branch level. COU_177, COU_184 and COU_170; Tabulado row 48.', 'https://www.inegi.org.mx/programas/cou/2018/'),
            ('[3] INEGI. SCIAN Mexico 2018, printed pp. 150-151 (PDF pp. 169-170), categories 3115 and 311513.', sources['classification']['url']),
        ]),
    ]


def md_text(blocks):
    parts = []
    for block in blocks:
        kind = block[0]
        if kind == 'title':
            parts.append('# ' + block[1])
        elif kind == 'heading':
            parts.append('## ' + block[1])
        elif kind == 'lead':
            parts.append('**' + block[1] + '**')
        elif kind in ('meta', 'p', 'small'):
            parts.append(block[1])
        elif kind == 'table':
            rows = block[1]
            lines = ['| ' + ' | '.join(s.replace('\n', ' ') for s in rows[0]) + ' |',
                     '| ' + ' | '.join('---' for _ in rows[0]) + ' |']
            lines.extend('| ' + ' | '.join(s.replace('\n', ' ') for s in row) + ' |' for row in rows[1:])
            parts.append('\n'.join(lines))
        elif kind == 'figure':
            parts.append('![Intermediate uses of MIP 311513 by destination product group and origin, 2018.](' + block[1] + ')')
        elif kind == 'sources':
            parts.append('### Sources\n\n' + '\n\n'.join(f'{label} [Available at: {url}]({url})' for label, url in block[1]))
    return '\n\n'.join(parts) + '\n'


def paragraph_markup(text):
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', escape(text)).replace('\n', '<br/>')


def make_pdf(blocks):
    from reportlab import rl_config
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                   TableStyle, Image, PageBreak, KeepTogether)
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from matplotlib import font_manager
    rl_config.invariant = 1
    # Embed the same font family as the figure; avoid viewer font substitution.
    for name, weight in [('P04Sans', 'normal'), ('P04Sans-Bold', 'bold')]:
        font_path = font_manager.findfont(font_manager.FontProperties(family='DejaVu Sans', weight=weight))
        pdfmetrics.registerFont(TTFont(name, font_path))
    pdfmetrics.registerFontFamily('P04Sans', normal='P04Sans', bold='P04Sans-Bold',
                                 italic='P04Sans', boldItalic='P04Sans-Bold')
    width, height = A4
    doc = SimpleDocTemplate(str(ROOT / 'NOTE.pdf'), pagesize=A4,
                            rightMargin=60, leftMargin=60, topMargin=48, bottomMargin=48,
                            title=TITLE, author='Isaac Guzmán Valdivia Tovar',
                            subject='Mexico MIP 2018, imported-origin exposure by use')
    styles = {
        'title': ParagraphStyle('title', fontName='P04Sans-Bold', fontSize=21.5, leading=25,
                                textColor=colors.HexColor(NAVY), spaceAfter=10),
        'meta': ParagraphStyle('meta', fontName='P04Sans', fontSize=7.8, leading=11,
                               textColor=colors.HexColor('#5A6675'), spaceAfter=12),
        'lead': ParagraphStyle('lead', fontName='P04Sans-Bold', fontSize=11.5, leading=16,
                               textColor=colors.HexColor(NAVY), spaceAfter=12),
        'heading': ParagraphStyle('heading', fontName='P04Sans-Bold', fontSize=11.4, leading=15,
                                  textColor=colors.HexColor(NAVY), spaceBefore=7, spaceAfter=7,
                                  keepWithNext=True),
        'p': ParagraphStyle('p', fontName='P04Sans', fontSize=9.2, leading=13.0,
                            textColor=colors.HexColor(INK), spaceAfter=8),
        'small': ParagraphStyle('small', fontName='P04Sans', fontSize=7.3, leading=10,
                                textColor=colors.HexColor('#526071'), spaceAfter=8),
        'cell': ParagraphStyle('cell', fontName='P04Sans', fontSize=7.8, leading=10.6,
                               textColor=colors.HexColor(INK)),
        'cellnum': ParagraphStyle('cellnum', fontName='P04Sans', fontSize=8.0, leading=10.6,
                                  textColor=colors.HexColor(INK), alignment=TA_RIGHT),
        'head': ParagraphStyle('head', fontName='P04Sans-Bold', fontSize=7.6, leading=10,
                               textColor=colors.white),
    }
    story = []
    for block in blocks:
        kind = block[0]
        if kind in styles:
            story.append(Paragraph(paragraph_markup(block[1]), styles[kind]))
        elif kind == 'page':
            story.append(PageBreak())
        elif kind == 'table':
            rows, widths = block[1:]
            formatted = []
            numeric_table = rows[0][0] != 'Economic question'
            for i, row in enumerate(rows):
                formatted.append([Paragraph(paragraph_markup(s), styles['head'] if i == 0 else
                                            styles['cellnum'] if numeric_table and j > 0 else styles['cell'])
                                  for j, s in enumerate(row)])
            t = Table(formatted, colWidths=widths, hAlign='LEFT', repeatRows=1)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(NAVY)),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#EEF2F7'), colors.white]),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7),
                ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
                ('LINEBELOW', (0, 0), (-1, -1), .5, colors.white),
            ]))
            story.extend([t, Spacer(1, 6)])
        elif kind == 'figure':
            story.append(Image(str(ROOT / block[1]), width=475, height=262.5))
            story.append(Spacer(1, 4))
        elif kind == 'sources':
            for label, url in block[1]:
                # Stable numbered references keep long download URLs out of the layout.
                story.append(Paragraph(escape(label) + ' <link href="' + escape(url) +
                                       '" color="#002060">Official source</link>.', styles['small']))

    def footer(canvas, current_doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor('#D5DEEA'))
        canvas.setLineWidth(.5)
        canvas.line(60, 34, width - 60, 34)
        canvas.setFont('P04Sans', 7.0)
        canvas.setFillColor(colors.HexColor('#5A6675'))
        canvas.drawString(60, 22, 'P04 | Independent analysis | INEGI data: 2018')
        canvas.drawRightString(width - 60, 22, str(current_doc.page))
        canvas.restoreState()
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def main():
    evidence = load_evidence()
    make_figure(evidence[1])
    blocks = make_blocks(evidence)
    (ROOT / 'NOTE.md').write_text(md_text(blocks), encoding='utf-8')
    make_pdf(blocks)
    outputs = ['NOTE.md', 'NOTE.pdf', 'figures/intermediate_destination_origins.png',
               'figures/intermediate_destination_origins.svg']
    record = {
        'data_year': 2018, 'project_review_date': '2026-10-26',
        'builder': 'build_publication.py',
        'figure_source': 'results/intermediate_destination_groups.csv',
        'figure_source_sha256': sha(ROOT / 'results/intermediate_destination_groups.csv'),
        'input_sha256': sha(ROOT / 'data/official_cells.csv'),
        'outputs': {name: sha(ROOT / name) for name in outputs},
        'scope': 'Numerical text, tables and figure generated from validated CSV results; visual inspection is recorded separately in VALIDATION.md.'
    }
    (ROOT / 'results/publication_manifest.json').write_text(json.dumps(record, indent=2)+'\n')
    print('Built NOTE.md, NOTE.pdf and the destination figure from P04 results.')


if __name__ == '__main__':
    main()
