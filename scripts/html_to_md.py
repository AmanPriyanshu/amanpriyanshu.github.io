#!/usr/bin/env python3
"""
HTML to Markdown converter for amanpriyanshu.github.io
Tailored to extract structured content from the personal website
"""

from bs4 import BeautifulSoup
import re

def clean_text(text):
    """Clean and normalize text content"""
    if not text:
        return ""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_links(element):
    """Extract text with markdown links"""
    result = []
    for child in element.children:
        if child.name == 'a':
            href = child.get('href', '')
            text = clean_text(child.get_text())
            if text:
                result.append(f"[{text}]({href})")
        elif child.name == 'br':
            result.append('\n')
        elif hasattr(child, 'get_text'):
            result.append(clean_text(child.get_text()))
        else:
            result.append(str(child))
    return ''.join(result)

def convert_html_to_markdown(html_path, output_path):
    """Convert the HTML website to a structured markdown document"""
    
    with open(html_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    md_lines = []
    
    # Header
    md_lines.append("# Aman Priyanshu - AI Researcher")
    md_lines.append("")
    
    # Extract hero section
    hero = soup.find('section', class_='hero')
    if hero:
        # Name and title
        hero_text = hero.find('div', class_='hero-text')
        if hero_text:
            h2 = hero_text.find('h2')
            if h2:
                md_lines.append(f"## {clean_text(h2.get_text())}")
                md_lines.append("")
            
            # Bio paragraph
            bio = hero_text.find('p', id='bioParagraph')
            if bio:
                bio_content = extract_links(bio)
                md_lines.append(bio_content)
                md_lines.append("")
    
    # Contact & Links
    md_lines.append("## Contact & Links")
    md_lines.append("")
    hero_links = soup.find('div', class_='hero-links')
    if hero_links:
        links_list = []
        for link in hero_links.find_all('a'):
            href = link.get('href', '')
            title = link.get('title', '')
            if 'mailto:' in href:
                email = href.replace('mailto:', '')
                links_list.append(f"- Email: {email}")
            elif title:
                links_list.append(f"- {title}: {href}")
        md_lines.extend(links_list)
        md_lines.append("")
    
    # Resume link
    resume_link = soup.find('div', class_='resume-link')
    if resume_link:
        resume_a = resume_link.find('a')
        if resume_a:
            md_lines.append(f"- Resume: {resume_a.get('href', '')}")
            md_lines.append("")
    
    # Media Coverage
    media_section = soup.find('section', id='media')
    if media_section:
        md_lines.append("---")
        md_lines.append("")
        md_lines.append("## News & Media Coverage")
        md_lines.append("")
        
        media_cards = media_section.find_all('a', class_='media-card')
        for card in media_cards:
            source = card.find('span', class_='source-tag')
            title = card.find('h3')
            desc = card.find('p')
            url = card.get('href', '')
            
            if title:
                md_lines.append(f"### {clean_text(title.get_text())}")
                if source:
                    md_lines.append(f"*Source: {clean_text(source.get_text())}*")
                if desc:
                    md_lines.append(f"{clean_text(desc.get_text())}")
                md_lines.append(f"[Read more]({url})")
                md_lines.append("")
    
    # Publications
    pubs_section = soup.find('section', id='publications')
    if pubs_section:
        md_lines.append("---")
        md_lines.append("")
        md_lines.append("## Publications")
        md_lines.append("")
        
        pub_entries = pubs_section.find_all('div', class_='publication-entry')
        for entry in pub_entries:
            year_span = entry.find('span', class_='publication-year')
            title = entry.find('h3')
            
            if year_span and title:
                year = clean_text(year_span.get_text())
                title_link = title.find('a')
                if title_link:
                    title_text = clean_text(title_link.get_text())
                    url = title_link.get('href', '')
                    md_lines.append(f"### [{title_text}]({url})")
                else:
                    md_lines.append(f"### {clean_text(title.get_text())}")
                
                md_lines.append(f"**Year:** {year}")
                
                # Authors and venue
                paragraphs = entry.find_all('p')
                for p in paragraphs:
                    text = clean_text(p.get_text())
                    if text:
                        md_lines.append(text)
                md_lines.append("")
    
    # Blogs
    blogs_section = soup.find('section', id='blogs')
    if blogs_section:
        md_lines.append("---")
        md_lines.append("")
        md_lines.append("## Curated Blogs")
        md_lines.append("")
        
        blog_cards = blogs_section.find_all('a', class_='blog-card')
        for card in blog_cards:
            title = card.find('h3')
            desc = card.find('p')
            url = card.get('href', '')
            
            if title:
                title_text = clean_text(title.get_text())
                md_lines.append(f"### [{title_text}]({url})")
                if desc:
                    md_lines.append(f"{clean_text(desc.get_text())}")
                md_lines.append("")
    
    # Experience
    exp_section = soup.find('section', id='experience')
    if exp_section:
        md_lines.append("---")
        md_lines.append("")
        md_lines.append("## Experience")
        md_lines.append("")
        
        timeline_items = exp_section.find_all('div', class_='timeline-item')
        for item in timeline_items:
            h3 = item.find('h3')
            h4 = item.find('h4')
            date = item.find('p')
            
            if h3:
                title_link = h3.find('a')
                if title_link:
                    title_text = clean_text(title_link.get_text())
                    url = title_link.get('href', '')
                    md_lines.append(f"### [{title_text}]({url})")
                else:
                    md_lines.append(f"### {clean_text(h3.get_text())}")
            
            if h4:
                md_lines.append(f"**Organization:** {clean_text(h4.get_text())}")
            if date:
                md_lines.append(f"**Duration:** {clean_text(date.get_text())}")
            md_lines.append("")
    
    # Education
    edu_section = soup.find('section', id='education')
    if edu_section:
        md_lines.append("---")
        md_lines.append("")
        md_lines.append("## Education")
        md_lines.append("")
        
        edu_entries = edu_section.find_all('div', class_='education-entry')
        for entry in edu_entries:
            h3 = entry.find('h3')
            h4 = entry.find('h4')
            
            if h3:
                md_lines.append(f"### {clean_text(h3.get_text())}")
            if h4:
                md_lines.append(f"**Degree:** {clean_text(h4.get_text())}")
            
            # Key courses
            paragraphs = entry.find_all('p')
            for p in paragraphs:
                text = clean_text(p.get_text())
                if text:
                    md_lines.append(text)
            md_lines.append("")
    
    # Projects
    proj_section = soup.find('section', id='projects')
    if proj_section:
        md_lines.append("---")
        md_lines.append("")
        md_lines.append("## Relevant Projects")
        md_lines.append("")
        
        proj_entries = proj_section.find_all('div', class_='project-entry')
        for entry in proj_entries:
            h3 = entry.find('h3')
            
            if h3:
                title_link = h3.find('a')
                if title_link:
                    title_text = clean_text(title_link.get_text())
                    url = title_link.get('href', '')
                    md_lines.append(f"### [{title_text}]({url})")
                else:
                    md_lines.append(f"### {clean_text(h3.get_text())}")
            
            paragraphs = entry.find_all('p')
            for p in paragraphs:
                text = clean_text(p.get_text())
                if text and 'publication-year' not in p.get('class', []):
                    md_lines.append(text)
            md_lines.append("")
    
    # Achievements
    achieve_section = soup.find('section', id='achievements')
    if achieve_section:
        md_lines.append("---")
        md_lines.append("")
        md_lines.append("## Achievements")
        md_lines.append("")
        
        achieve_entries = achieve_section.find_all('div', class_='project-entry')
        for entry in achieve_entries:
            h3 = entry.find('h3')
            
            if h3:
                title_link = h3.find('a')
                if title_link:
                    title_text = clean_text(title_link.get_text())
                    url = title_link.get('href', '')
                    md_lines.append(f"### [{title_text}]({url})")
                else:
                    md_lines.append(f"### {clean_text(h3.get_text())}")
            
            paragraphs = entry.find_all('p')
            for p in paragraphs:
                text = clean_text(p.get_text())
                if text:
                    md_lines.append(text)
            md_lines.append("")
    
    # Demos
    demos_section = soup.find('section', id='demos')
    if demos_section:
        md_lines.append("---")
        md_lines.append("")
        md_lines.append("## Interactive Tools/Demos & Games")
        md_lines.append("")
        
        game_cards = demos_section.find_all('a', class_='game-card')
        for card in game_cards:
            title = card.find('h3')
            desc = card.find('p')
            url = card.get('href', '')
            
            if title:
                title_text = clean_text(title.get_text())
                md_lines.append(f"### [{title_text}]({url})")
                if desc:
                    md_lines.append(f"{clean_text(desc.get_text())}")
                md_lines.append("")
    
    # Footer
    md_lines.append("---")
    md_lines.append("")
    md_lines.append("*© 2024 Aman Priyanshu. All rights reserved.*")
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_lines))
    
    print(f"✓ Markdown file generated: {output_path}")
    print(f"✓ Total lines: {len(md_lines)}")

if __name__ == "__main__":
    convert_html_to_markdown('index.html', 'llm-markdown.md')